# services/discussion_service.py
from bson import ObjectId
from models.discussion_model import Discussion, Reply
from schemas.discussion_schema import DiscussionCreate, ReplyCreate
from models.user_model import User

async def create_discussion(user_id: str, data: DiscussionCreate) -> Discussion:
    discussion = Discussion(
        user_id=ObjectId(user_id),
        title=data.title,
        content=data.content,
        created_at=data.created_at
    )
    await discussion.insert()
    return discussion

async def get_discussion_by_id(discussion_id: str) -> Discussion | None:
    return await Discussion.get(ObjectId(discussion_id))

async def add_reply(discussion_id: str, user_id: str, data: ReplyCreate) -> Discussion | None:
    discussion = await Discussion.get(ObjectId(discussion_id))
    if not discussion:
        return None
    reply = Reply(user_id=ObjectId(user_id), content=data.content, created_at=data.created_at)
    discussion.replies.append(reply)
    await discussion.save()
    return discussion

async def get_all_discussions_with_usernames():
    discussions = await Discussion.find_all().sort("-created_at").to_list()
    response = []

    for d in discussions:
        user = await User.get(d.user_id)
        replies_with_usernames = []
        for r in d.replies:
            reply_user = await User.get(r.user_id)
            replies_with_usernames.append({
                "user_id": str(r.user_id),
                "username": reply_user.username if reply_user else None,
                "content": r.content,
                "created_at": r.created_at
            })
        
        response.append({
            "id": str(d.id),
            "user_id": str(d.user_id),
            "username": user.username if user else None,
            "title": d.title,
            "content": d.content,
            "replies": replies_with_usernames,
            "created_at": d.created_at
        })
    
    return response

async def update_discussion_content(discussion_id: str, user_id: str, data: DiscussionCreate) -> Discussion | None:
    discussion = await Discussion.get(ObjectId(discussion_id))
    if not discussion or discussion.user_id != ObjectId(user_id):
        return None
    
    discussion.title = data.title
    discussion.content = data.content
    await discussion.save()
    return discussion

async def delete_discussion_by_id(discussion_id: str, user_id: str) -> bool:
    discussion = await Discussion.get(ObjectId(discussion_id))
    if not discussion or discussion.user_id != ObjectId(user_id):
        return False
    
    await discussion.delete()
    return True