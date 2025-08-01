from fastapi import APIRouter, Depends, HTTPException
from typing import List

from schemas.discussion_schema import DiscussionCreate, DiscussionResponse, ReplyCreate, ReplyResponse
from services.discussion_service import (
    create_discussion, get_all_discussions_with_usernames,
    get_discussion_by_id, add_reply
)
from utils.security import get_current_user 
from models.user_model import User 

router = APIRouter()

@router.post("/", response_model=DiscussionResponse, status_code=201)
async def create_new_discussion(
    data: DiscussionCreate,
    current_user: User = Depends(get_current_user)
):
    discussion = await create_discussion(current_user.id, data)
    return DiscussionResponse(
        id=str(discussion.id),
        user_id=str(discussion.user_id),
        title=discussion.title,
        content=discussion.content,
        replies=[],
        created_at=discussion.created_at
    )

@router.get("/", response_model=List[DiscussionResponse])
async def list_discussions():
    discussions = await get_all_discussions_with_usernames()

    # konversi setiap dict menjadi Pydantic model
    return [
        DiscussionResponse(
            id=str(d["id"]),
            user_id=str(d["user_id"]),
            username=d["username"],
            title=d["title"],
            content=d["content"],
            created_at=d["created_at"],
            replies=[
                ReplyResponse(
                    user_id=str(r["user_id"]),
                    username=r["username"],
                    content=r["content"],
                    created_at=r["created_at"]
                )
                for r in d["replies"]
            ]
        )
        for d in discussions
    ]



@router.post("/{discussion_id}/reply", response_model=DiscussionResponse)
async def reply_to_discussion(
    discussion_id: str,
    data: ReplyCreate,
    current_user: User = Depends(get_current_user)
):
    updated = await add_reply(discussion_id, current_user.id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Discussion not found")
    
    return DiscussionResponse(
        id=str(updated.id),
        user_id=str(updated.user_id),
        title=updated.title,
        content=updated.content,
        replies=[{
            "user_id": str(r.user_id),
            "content": r.content,
            "created_at": r.created_at
        } for r in updated.replies],
        created_at=updated.created_at
    )
