# Feature_Extraction_PWShell_Script

---
## 추출할 피처 고를때 고려사항
1. 가급적 많은 피처 뽑기 (어차피, feature importance 계산함)
2. sparsity가 높은 피처는 ㄴㄴ
3. uniqueness가 높은 피처도 ㄴㄴ

---
## 추출할만한 피처
1. TOP N 단어 frequency (e.g., TF-IDF)
2. 스트링 엔트로피
3. 특정 변수, 메서드명
4. 특수문자 개수
5. URL
6. IP
7. 알려진 악성프로그램명
8. 그외 파워쉘 스크립트의 특징


---
## 결론
- 사실, 정답은 없고 여러 방식으로 해보고 테스트 및 연습해보는 과정 필요할 듯
