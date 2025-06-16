import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

# ---------------------
# EDA 페이지 클래스
# ---------------------
class EDA:
    def __init__(self):
        st.title("📊 Population Trends Analysis")
        uploaded = st.file_uploader("데이터셋 업로드 (population_trends.csv)", type="csv")
        if not uploaded:
            st.info("population_trends.csv 파일을 업로드 해주세요.")
            return

        df = pd.read_csv(uploaded)

        tabs = st.tabs([
            "1. 기초 통계",
            "2. 연도별 추이",
            "3. 지역별 분석",
            "4. 변화량 분석",
            "5. 시각화"
        ])

        # 1. 기초 통계
        with tabs[0]:
            st.header("📈 기초 통계")
            
            # 데이터 구조 확인
            st.subheader("데이터 구조")
            buffer = io.StringIO()
            df.info(buf=buffer)
            st.text(buffer.getvalue())

            # 결측치 확인
            st.subheader("결측치 확인")
            missing = df.isnull().sum()
            st.bar_chart(missing)
            
            # 중복 확인
            duplicates = df.duplicated().sum()
            st.write(f"- 중복 행 개수: {duplicates}개")

            # 기초 통계량
            st.subheader("기초 통계량")
            st.dataframe(df.describe())

        # 2. 연도별 추이
        with tabs[1]:
            st.header("📅 연도별 추이")
            
            # 연도별 전체 인구 추이 그래프
            yearly_total = df.groupby('year')['population'].sum().reset_index()
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(data=yearly_total, x='year', y='population', marker='o')
            plt.title('연도별 전체 인구 추이')
            plt.xlabel('연도')
            plt.ylabel('인구')
            plt.grid(True)
            st.pyplot(fig)

            # 연도별 통계
            st.subheader("연도별 통계")
            yearly_stats = df.groupby('year').agg({
                'population': ['mean', 'min', 'max', 'std']
            }).round(2)
            st.dataframe(yearly_stats)

        # 3. 지역별 분석
        with tabs[2]:
            st.header("🗺️ 지역별 분석")
            
            # 지역별 평균 인구
            region_avg = df.groupby('region')['population'].mean().sort_values(ascending=False)
            
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(x=region_avg.index, y=region_avg.values)
            plt.title('지역별 평균 인구')
            plt.xticks(rotation=45)
            plt.xlabel('지역')
            plt.ylabel('평균 인구')
            st.pyplot(fig)

            # 지역별 최대/최소 인구
            st.subheader("지역별 최대/최소 인구")
            region_stats = df.groupby('region').agg({
                'population': ['max', 'min']
            }).round(2)
            st.dataframe(region_stats)

        # 4. 변화량 분석
        with tabs[3]:
            st.header("📊 변화량 분석")
            
            # 연도별 변화량 계산
            df['year'] = pd.to_numeric(df['year'])
            df = df.sort_values(['region', 'year'])
            df['population_change'] = df.groupby('region')['population'].diff()
            df['change_rate'] = (df['population_change'] / df['population'].shift(1) * 100).round(2)

            # 변화량 상위 지역
            st.subheader("인구 변화량 상위 지역")
            top_changes = df.nlargest(10, 'population_change')[['region', 'year', 'population_change']]
            st.dataframe(top_changes)

            # 증감률 상위 지역
            st.subheader("인구 증감률 상위 지역")
            top_rates = df.nlargest(10, 'change_rate')[['region', 'year', 'change_rate']]
            st.dataframe(top_rates)

        # 5. 시각화
        with tabs[4]:
            st.header("🎨 시각화")
            
            # 누적 영역 그래프
            st.subheader("지역별 인구 누적 추이")
            pivot_df = df.pivot(index='year', columns='region', values='population')
            
            fig, ax = plt.subplots(figsize=(12, 6))
            pivot_df.plot(kind='area', stacked=True, ax=ax)
            plt.title('지역별 인구 누적 추이')
            plt.xlabel('연도')
            plt.ylabel('인구')
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            st.pyplot(fig)

            # 히트맵
            st.subheader("연도-지역 인구 히트맵")
            pivot_df = df.pivot_table(index='year', columns='region', values='population')
            
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.heatmap(pivot_df, annot=True, fmt='.0f', cmap='YlOrRd')
            plt.title('연도-지역 인구 히트맵')
            st.pyplot(fig)

# ---------------------
# 페이지 실행
# ---------------------
if __name__ == "__main__":
    eda = EDA()