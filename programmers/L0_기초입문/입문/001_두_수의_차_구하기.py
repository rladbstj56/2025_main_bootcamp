# 두 수의 차 구하기
# 프로그래머스 L0 (기초·입문)
# 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/120803
# 알고리즘: 기초
# 작성자: 김윤서
# 작성일: 2026. 01. 19. 11:17:40

def solution(num1, num2):
    if num1>50000 or num1<-50000 or num2>50000 or num2<-50000:
        return False
    answer = num1 - num2
    return answer