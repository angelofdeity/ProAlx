from sqlalchemy import Integer, Column, VARCHAR, ForeignKey, String
from sqlalchemy.orm import relationship
from backend.api.v1.views.git_stats import username
from .base_model import BaseModel
from api.v1.views.git_stats import get_commits


class User(BaseModel):
    __tablename__ = 'users'

    # use github display name and photo by default
    name = Column(String(50), nullable=False)
    photo_url = Column(String(255))

    username = Column(String(50), unique=True)
    twitter_username = Column(String(255))
    whatsapp = Column(String(25))
    email = Column(String(255))
    github_uid = Column(Integer)
    wakatime_uid = Column(String(255))
    gh_access_token = Column(String(255))
    wk_access_token = Column(String(255))
    wk_refresh_token = Column(String(255))
    likes_interests = Column(String(255))
    most_active_time = Column(String(10))
    timezone = Column(String(50))  # default could be from github/wakatime
    github_session = Column(String(255))
    waka_session = Column(String(255))
    github_login = Column(String(255))
    wakatime_login = Column(String(255))
    interests = Column(String(255))
    cohort_id = Column(String(60), ForeignKey('cohorts.id'))

    cohort = relationship("Cohort", back_populates="users")

    def fetch_github_data(self):
        """Retrives daily commits of user from github api"""
        token = self.gh_access_token
        username = self.github_login
        if not token or not username:
            return None
        return get_commits(token, username)
