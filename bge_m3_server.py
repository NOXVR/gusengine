"""
V10-compliant BGE-M3 Embedding Server with Dense + Sparse support.

Implements the TEI-compatible API:
- POST /embed        -> dense vectors (1024-dim)
- POST /embed_sparse -> sparse vectors (indices + values)
- GET  /health       -> health check

Uses FlagEmbedding's BGEM3FlagModel which natively supports BGE-M3's
multi-vector output: dense, sparse (lexical weights), and colbert.
"""
import json
import logging
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from FlagEmbedding import BGEM3FlagModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

MODEL_PATH = os.environ.get("BGE_M3_MODEL_PATH", "/workspace/GusEngine/storage/models/bge-m3")
PORT = int(os.environ.get("TEI_PORT", "8080"))

logger.info(f"Loading BGE-M3 from {MODEL_PATH}...")
model = BGEM3FlagModel(MODEL_PATH, use_fp16=True)
logger.info("BGE-M3 model loaded successfully")


class EmbeddingHandler(BaseHTTPRequestHandler):
    """TEI-compatible HTTP handler for BGE-M3 embeddings."""

    def do_GET(self):
        """Health check endpoint."""
        if self.path == "/health" or self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        """Embedding endpoints: /embed (dense) and /embed_sparse (sparse)."""
        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length))

        # TEI format: {"inputs": "text"} or {"inputs": ["text1", "text2"]}
        inputs = body.get("inputs", "")
        if isinstance(inputs, str):
            inputs = [inputs]

        try:
            if self.path == "/embed":
                # Dense embeddings (1024-dim for BGE-M3)
                output = model.encode(
                    inputs,
                    return_dense=True,
                    return_sparse=False,
                    return_colbert_vecs=False,
                )
                dense_vectors = output["dense_vecs"].tolist()
                self._respond_json(dense_vectors)

            elif self.path == "/embed_sparse":
                # Sparse embeddings (lexical weights)
                output = model.encode(
                    inputs,
                    return_dense=False,
                    return_sparse=True,
                    return_colbert_vecs=False,
                )
                # output["lexical_weights"] is a list of dicts: {token_id: weight}
                sparse_results = []
                for weights_dict in output["lexical_weights"]:
                    # Convert to TEI-compatible format: list of {"index": int, "value": float}
                    sparse_vec = [
                        {"index": int(idx), "value": float(val)}
                        for idx, val in weights_dict.items()
                    ]
                    sparse_results.append(sparse_vec)
                self._respond_json(sparse_results)

            else:
                self.send_response(404)
                self.end_headers()
                return

        except Exception as e:
            logger.error(f"Embedding error: {e}")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def _respond_json(self, data):
        """Send JSON response."""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        """Suppress per-request logging to reduce noise."""
        pass


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), EmbeddingHandler)
    logger.info(f"BGE-M3 embedding server listening on port {PORT}")
    logger.info(f"Endpoints: /embed (dense), /embed_sparse (sparse), /health")
    server.serve_forever()
