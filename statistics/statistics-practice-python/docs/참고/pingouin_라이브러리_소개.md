# pingouin 라이브러리 개요

## 공식 문서 및 참고 링크

- **공식 문서**: https://pingouin-stats.org/
- **API 레퍼런스**: https://pingouin-stats.org/build/html/api.html

---

## pingouin이란?

pingouin은 Python 기반의 통계 분석 라이브러리로, **한 줄 호출 → pandas DataFrame 반환**이라는 설계 철학을 가지고 있습니다. scipy.stats가 (통계량, p-value) 튜플을 반환하는 것과 달리, pingouin은 검정 결과를 **효과 크기·신뢰구간·베이즈 팩터까지 포함한 표**로 한꺼번에 제공합니다.

## SciPy · statsmodels와의 관계

| 라이브러리 | 역할 |
|-----------|------|
| **SciPy** | 확률분포, 개별 통계검정 (튜플 반환) |
| **statsmodels** | 회귀 모델링, 상세 요약표, 진단 도구 |
| **pingouin** | 검정 + 효과 크기 + 베이즈 팩터를 DataFrame 한 줄로 반환 |

- SciPy: `stats.ttest_ind(g1, g2)` → `(t_stat, p_value)` 튜플
- statsmodels: `OLS(y, X).fit().summary()` → 상세 회귀 요약표
- pingouin: `pg.ttest(g1, g2)` → T, dof, tail, p-val, CI95%, cohen-d, BF10, power 포함 DataFrame

## 설치

둘 중 하나를 선택하여 설치합니다.

```bash
uv add pingouin
```

```bash
pip install pingouin
```

---

## 주요 기능 영역

| 영역 | 주요 함수 |
|------|-----------|
| t-검정 | `pg.ttest()` |
| 분산분석 | `pg.anova()`, `pg.welch_anova()`, `pg.rm_anova()`, `pg.mixed_anova()` |
| 비모수 검정 | `pg.mwu()`, `pg.wilcoxon()`, `pg.kruskal()`, `pg.friedman()` |
| 사후검정 | `pg.pairwise_tests()`, `pg.pairwise_tukey()`, `pg.pairwise_gameshowell()` |
| 상관분석 | `pg.corr()`, `pg.partial_corr()`, `pg.pcorr()` |
| 카이제곱 독립성 검정 | `pg.chi2_independence()`|
| 효과 크기 | `pg.compute_effsize()`, `pg.compute_effsize_from_t()` |
| 정규성·구형성 | `pg.normality()`, `pg.sphericity()`, `pg.homoscedasticity()` |
| 베이즈 통계 | 대부분의 검정 함수에 `BF10` (베이즈 팩터) 내장 |
| 신뢰구간 | `pg.compute_bootci()` (부트스트랩 CI) |
| 검정력 | `pg.power_ttest()`, `pg.power_anova()`, `pg.power_chi2()` |
---

## 통계 실습에서 자주 쓰는 기능

### 1. 가정 검정 (정규성 · 등분산)

```python
import pingouin as pg

# 정규성 검정 (Shapiro-Wilk)
pg.normality(data, dv='score', group='group')
# → DataFrame: W, pval, normal (bool)

# 등분산 검정 (Levene)
pg.homoscedasticity(data, dv='score', group='group')
# → DataFrame: equal_var (bool), p-val

# 구형성 검정 (반복측정용)
pg.sphericity(data, dv='score', subject='id', within='time')
```

### 2. t-검정

```python
# 독립표본 t-검정
pg.ttest(g1, g2, paired=False, alternative='two-sided')
# → T, dof, tail, p-val, CI95%, cohen-d, BF10, power

# 대응표본 t-검정
pg.ttest(before, after, paired=True)

# 단일표본 t-검정
pg.ttest(data, y=0)   # y = 비교 기준값
```

> **핵심 장점**: cohen-d(효과 크기), BF10(베이즈 팩터), power(검정력)가 한꺼번에 반환됩니다.

### 3. 분산분석 (ANOVA)

```python
# 일원 분산분석
pg.anova(data, dv='score', between='group', detailed=True)
# → Source, SS, DF, MS, F, p-unc, np2(η²)

# Welch's ANOVA (등분산 위반 시)
pg.welch_anova(data, dv='score', between='group')

# 반복측정 ANOVA
pg.rm_anova(data, dv='score', within='condition', subject='id',
            correction=True)  # Greenhouse-Geisser 보정

# 혼합 ANOVA (집단 간 + 반복측정)
pg.mixed_anova(data, dv='score', between='group',
               within='time', subject='id')
```

### 4. 비모수 검정

```python
# Mann-Whitney U (독립 2집단)
pg.mwu(g1, g2, alternative='two-sided')
# → U-val, p-val, RBC(rank-biserial correlation), CLES

# Wilcoxon signed-rank (대응표본)
pg.wilcoxon(before, after, alternative='two-sided')
# → W-val, p-val, RBC, CLES

# Kruskal-Wallis (독립 3집단+)
pg.kruskal(data, dv='score', between='group')

# Friedman (반복측정 비모수)
pg.friedman(data, dv='score', within='condition', subject='id')
```

> **핵심 장점**: 비모수 검정에서도 **효과 크기(RBC)** 와 **CLES(공통 언어 효과 크기)** 가 자동 포함됩니다.

### 5. 사후검정 (다중비교)

```python
# Tukey HSD (ANOVA 후, 등분산 만족)
pg.pairwise_tukey(data, dv='score', between='group')
# → A, B, mean(A), mean(B), diff, se, T, p-tukey, hedges

# Games-Howell (등분산 위반 시)
pg.pairwise_gameshowell(data, dv='score', between='group')
# → A, B, mean(A), mean(B), diff, se, T, df, pval, hedges

# 범용 쌍별 비교 (모수/비모수 자동 선택)
pg.pairwise_tests(data, dv='score', between='group',
                  parametric=True,     # False → 비모수
                  padjust='bonf')      # 다중비교 보정 방법
# padjust 옵션: 'bonf', 'holm', 'fdr_bh', 'fdr_by', 'none'
```

### 6. 상관분석

```python
# Pearson / Spearman / Kendall 상관
pg.corr(x, y, method='pearson')
# → n, r, CI95%, p-val, BF10, power

# 편상관 (제3변수 통제)
pg.partial_corr(data, x='x', y='y', covar='z')

# 상관행렬 (모든 쌍)
pg.pairwise_corr(data, columns=['x', 'y', 'z'], method='pearson')
```

### 7. 효과 크기

```python
# Cohen's d 직접 계산
pg.compute_effsize(g1, g2, eftype='cohen')
# eftype: 'cohen', 'hedges', 'r', 'eta-square', 'odds-ratio', 'AUC', 'CLES'

# t-통계량으로부터 효과 크기 계산
pg.compute_effsize_from_t(t_stat, nx=30, ny=30, eftype='cohen')
```

### 8. 검정력 분석

```python
# t-검정 검정력
pg.power_ttest(d=0.5, n=30, alpha=0.05, alternative='two-sided')

# 필요 표본크기 (power → n)
pg.power_ttest(d=0.5, power=0.8, alpha=0.05)

# ANOVA 검정력
pg.power_anova(eta_squared=0.06, k=3, n=30, alpha=0.05)

# 카이제곱 검정력
pg.power_chi2(w=0.3, n=100, dof=2, alpha=0.05)
```

### 9. 부트스트랩 신뢰구간

```python
# 부트스트랩 CI (임의의 함수에 적용 가능)
ci = pg.compute_bootci(data, func='mean', n_boot=2000,
                        confidence=0.95, seed=42)
# → [lower, upper]

# 중앙값 CI
ci = pg.compute_bootci(data, func='median')
```

---

## SciPy vs statsmodels vs pingouin 비교

| 작업 | SciPy | statsmodels | pingouin |
|------|-------|-------------|----------|
| 독립 t-검정 | `ttest_ind()` → 튜플 | `ttest_ind()` | `ttest()` → DataFrame (d, BF10, power 포함) |
| 효과 크기 | 직접 계산 | 직접 계산 | **자동 포함** (cohen-d, η², RBC) |
| 베이즈 팩터 | 없음 | 없음 | **자동 포함** (BF10) |
| Welch's ANOVA | 없음 | `anova_oneway(use_var='unequal')` | `welch_anova()` |
| Games-Howell | 없음 | 없음 | `pairwise_gameshowell()` |
| 반복측정 ANOVA | 없음 | 수식 기반 | `rm_anova()` (GG 보정 포함) |
| 혼합 ANOVA | 없음 | 수식 기반 | `mixed_anova()` |
| 비모수 효과 크기 | 직접 계산 | 직접 계산 | **자동 포함** (RBC, CLES) |
| 정규성 검정 | `shapiro()` → 튜플 | `jarque_bera()` | `normality()` → DataFrame (bool 포함) |
| 등분산 검정 | `levene()` → 튜플 | 없음 | `homoscedasticity()` → DataFrame (bool 포함) |
| 부트스트랩 CI | 없음 | 없음 | `compute_bootci()` |
| 반환 형식 | 튜플 | 모델 객체 | **pandas DataFrame** |

---

## 언제 어떤 라이브러리를 쓰는가?

| 상황 | 추천 라이브러리 |
|------|----------------|
| 확률분포 계산 (pdf, cdf, ppf) | **SciPy** |
| 빠른 개별 검정 (t, χ², 상관) | **SciPy** |
| 회귀분석 상세 요약표 | **statsmodels** |
| 이원 이상 ANOVA (수식 기반) | **statsmodels** |
| 시계열 분석 (ARIMA) | **statsmodels** |
| 다중비교 p-value 보정 | **statsmodels** (`multipletests`) |
| 효과 크기·베이즈 팩터 포함 검정 | **pingouin** |
| Games-Howell 사후검정 | **pingouin** |
| 반복측정·혼합 ANOVA | **pingouin** |
| 비모수 검정 + 효과 크기 | **pingouin** |
| 부트스트랩 신뢰구간 | **pingouin** |
