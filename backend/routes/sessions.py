# backend/routes/sessions.py
# Diagnostic Session Persistence — save/load/list/delete full diagnostic jobs
# Patent Claim #9: Byte-for-byte snapshot of diagnostic state
import json
import logging
import os
import time
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Request

logger = logging.getLogger(__name__)

router = APIRouter()

# Session storage directory — JSON files, one per session
_SESSIONS_DIR = os.environ.get("SESSIONS_DIR", "/app/sessions")
os.makedirs(_SESSIONS_DIR, exist_ok=True)
logger.info(f"Session storage: {_SESSIONS_DIR}")


def _session_path(session_id: str) -> str:
    """Get the file path for a session by ID. Validates ID format."""
    # Prevent path traversal
    safe_id = os.path.basename(session_id)
    if not safe_id or safe_id != session_id:
        raise ValueError(f"Invalid session ID: {session_id}")
    return os.path.join(_SESSIONS_DIR, f"{safe_id}.json")


def _load_session(session_id: str) -> dict | None:
    """Load a session from disk. Returns None if not found."""
    path = _session_path(session_id)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)


def _save_session(session: dict) -> str:
    """Save a session to disk. Returns the session_id."""
    session_id = session["session_id"]
    session["updated_at"] = datetime.now(timezone.utc).isoformat()
    path = _session_path(session_id)
    with open(path, "w") as f:
        json.dump(session, f, indent=2, default=str)
    logger.info(f"Session saved: {session_id} ({os.path.getsize(path)} bytes)")
    return session_id


@router.post("/api/session/save")
async def save_session(request: Request):
    """Save or update a diagnostic session.
    
    Accepts the full session state from the frontend. If session_id is provided,
    updates the existing session. If not, creates a new one.
    
    The frontend sends everything — chat_history, pending_issues, vehicle_id,
    resolved diagnostics. We store it byte-for-byte.
    """
    body = await request.json()
    
    session_id = body.get("session_id") or str(uuid.uuid4())
    
    # Build session object
    session = {
        "session_id": session_id,
        "vehicle_id": body.get("vehicle_id", ""),
        "vehicle_label": body.get("vehicle_label", ""),
        "created_at": body.get("created_at") or datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "status": body.get("status", "IN_PROGRESS"),
        "chat_history": body.get("chat_history", []),
        "pending_issues": body.get("pending_issues", []),
        "active_issue": body.get("active_issue"),
        "resolved_diagnostics": body.get("resolved_diagnostics", []),
        "token_count_estimate": body.get("token_count_estimate", 0),
        "summary": body.get("summary", ""),
    }
    
    _save_session(session)
    
    return {
        "session_id": session_id,
        "status": "saved",
        "updated_at": session["updated_at"],
    }


@router.get("/api/session/load/{session_id}")
async def load_session(session_id: str):
    """Load a saved diagnostic session by ID.
    
    Returns the complete session state — the frontend uses this to restore
    the chat history, pending issues, and vehicle context.
    """
    try:
        session = _load_session(session_id)
    except ValueError as e:
        return {"error": str(e)}, 400
    
    if session is None:
        return {"error": f"Session not found: {session_id}"}, 404
    
    logger.info(
        f"Session loaded: {session_id}, vehicle={session.get('vehicle_id')}, "
        f"messages={len(session.get('chat_history', []))}, "
        f"pending={len(session.get('pending_issues', []))}"
    )
    return session


@router.get("/api/session/list")
async def list_sessions(vehicle_id: str = None):
    """List all saved sessions, optionally filtered by vehicle.
    
    Returns summary info (not full chat histories) for performance.
    """
    sessions = []
    
    if not os.path.exists(_SESSIONS_DIR):
        return {"sessions": []}
    
    for filename in sorted(os.listdir(_SESSIONS_DIR), reverse=True):
        if not filename.endswith(".json"):
            continue
        
        filepath = os.path.join(_SESSIONS_DIR, filename)
        try:
            with open(filepath, "r") as f:
                session = json.load(f)
        except (json.JSONDecodeError, IOError):
            logger.warning(f"Corrupt session file: {filename}")
            continue
        
        # Filter by vehicle if requested
        if vehicle_id and session.get("vehicle_id") != vehicle_id:
            continue
        
        # Return summary only — not the full chat history
        sessions.append({
            "session_id": session.get("session_id"),
            "vehicle_id": session.get("vehicle_id"),
            "vehicle_label": session.get("vehicle_label", ""),
            "created_at": session.get("created_at"),
            "updated_at": session.get("updated_at"),
            "status": session.get("status"),
            "message_count": len(session.get("chat_history", [])),
            "pending_count": len([
                i for i in session.get("pending_issues", [])
                if i.get("status") != "RESOLVED"
            ]),
            "resolved_count": len(session.get("resolved_diagnostics", [])),
            "summary": session.get("summary", ""),
        })
    
    return {"sessions": sessions}


@router.delete("/api/session/delete/{session_id}")
async def delete_session(session_id: str):
    """Delete a saved session."""
    try:
        path = _session_path(session_id)
    except ValueError as e:
        return {"error": str(e)}, 400
    
    if not os.path.exists(path):
        return {"error": f"Session not found: {session_id}"}, 404
    
    os.remove(path)
    logger.info(f"Session deleted: {session_id}")
    return {"status": "deleted", "session_id": session_id}
