from sqlalchemy import Column, INTEGER, FLOAT
from sqlalchemy.dialects.mysql import VARCHAR
from app.models import Base, id_generate

class Score(Base):
    """成绩表"""
    __tablename__ = 'score'

    score_id = Column(INTEGER, default=id_generate, primary_key=True)  # 主键，自动生成
    student_id = Column(INTEGER, nullable=False)  # 学生 ID
    subject = Column(VARCHAR(100), nullable=False)  # 课程名称
    score_value = Column(FLOAT, nullable=False)  # 分数
    semester = Column(VARCHAR(50), nullable=False)  # 学期
    is_deleted = Column(VARCHAR(1), default='0')  # 是否删除，0=未删除，1=已删除
    status_id = Column(INTEGER, default=1)  # 状态 ID
    add_date = Column(VARCHAR(23))  # 添加时间
    add_user_id = Column(INTEGER)  # 添加人 ID
    edit_date = Column(VARCHAR(23))  # 编辑时间
    edit_user_id = Column(INTEGER)  # 编辑人 ID