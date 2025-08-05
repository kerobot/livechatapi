from typing import List, Optional
from pydantic import BaseModel


class AuthorDetails(BaseModel):
    channelId: str
    displayName: str
    profileImageUrl: str
    isVerified: Optional[bool] = False


class Snippet(BaseModel):
    type: str
    liveChatId: str
    authorChannelId: str
    publishedAt: str
    hasDisplayContent: bool
    displayMessage: str


class LiveChatMessageItem(BaseModel):
    kind: str
    etag: str
    id: str
    snippet: Snippet
    authorDetails: AuthorDetails


class PageInfo(BaseModel):
    totalResults: int
    resultsPerPage: int


class LiveChatMessageListResponse(BaseModel):
    kind: str
    etag: str
    nextPageToken: Optional[str] = None
    pollingIntervalMillis: int
    pageInfo: PageInfo
    items: List[LiveChatMessageItem]
