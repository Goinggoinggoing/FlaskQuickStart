# -*- coding: utf-8 -*-
"""
  Created by ByteBind on 2025/2/27.
"""
from app import db
from app.models.score import Score
from datetime import datetime


class ScoreDAO:
    """成绩数据访问对象"""

    @staticmethod
    def get_all():
        """获取所有未删除的成绩记录"""
        return db.session.query(Score).filter(Score.is_deleted == '0').all()

    @staticmethod
    def search(keyword=None, page=1, per_page=10):
        """
        根据关键字搜索成绩并分页

        Args:
            keyword: 搜索关键字
            page: 页码
            per_page: 每页记录数

        Returns:
            分页结果对象
        """
        query = db.session.query(Score).filter(Score.is_deleted == '0')

        if keyword:
            query = query.filter(Score.subject.like(f"%{keyword}%"))

        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_by_id(score_id):
        """
        通过ID获取成绩

        Args:
            score_id: 成绩ID

        Returns:
            Score对象 或 None
        """
        return db.session.query(Score).filter_by(score_id=score_id, is_deleted='0').first()

    @staticmethod
    def add(student_id, subject, score_value, semester, user_id=1):
        """
        添加新成绩

        Args:
            student_id: 学生ID
            subject: 科目
            score_value: 分数值
            semester: 学期
            user_id: 操作用户ID

        Returns:
            新创建的Score对象
        """
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        new_score = Score(
            student_id=student_id,
            subject=subject,
            score_value=score_value,
            semester=semester,
            is_deleted='0',
            status_id=1,
            add_date=current_time,
            add_user_id=user_id
        )

        db.session.add(new_score)
        db.session.commit()

        return new_score

    @staticmethod
    def update(score_id, score_value, user_id=1):
        """
        更新成绩

        Args:
            score_id: 成绩ID
            score_value: 新的分数值
            user_id: 操作用户ID

        Returns:
            更新后的Score对象 或 None（如果记录不存在）
        """
        score = ScoreDAO.get_by_id(score_id)

        if not score:
            return None

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        score.score_value = score_value
        score.edit_date = current_time
        score.edit_user_id = user_id

        db.session.commit()

        return score

    @staticmethod
    def delete(score_id):
        """
        软删除成绩

        Args:
            score_id: 成绩ID

        Returns:
            被删除的Score对象 或 None（如果记录不存在）
        """
        score = ScoreDAO.get_by_id(score_id)

        if not score:
            return None

        score.is_deleted = '1'
        db.session.commit()

        return score
