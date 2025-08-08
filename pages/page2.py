import streamlit as st
from datetime import date


st.title("企业数据")

# —— 表单开始 ——
with st.form("enterprise_form"):
    st.subheader("企业基本信息")

    # 基本信息：信用代码、名称、成立日期、行业、地区、规模
    col_a, col_b = st.columns(2)
    with col_a:
        credit_code = st.text_input("统一社会信用代码")
        company_name = st.text_input("企业名称")
        established_date = st.date_input("成立日期")
    with col_b:
        industry_options = [
            "制造业",
            "批发和零售业",
            "信息传输、软件和信息技术服务业",
            "建筑业",
            "住宿和餐饮业",
            "金融业",
            "房地产业",
            "租赁和商务服务业",
            "科学研究和技术服务业",
            "水利、环境和公共设施管理业",
            "交通运输、仓储和邮政业",
            "文化、体育和娱乐业",
            "采矿业",
            "电力、热力、燃气及水生产和供应业",
            "居民服务、修理和其他服务业",
            "农、林、牧、渔业",
            "教育",
            "卫生和社会工作",
            "公共管理、社会保障和社会组织",
            "其他",
        ]
        industry_category = st.selectbox("行业类别", options=industry_options, index=0)
        region = st.selectbox("所在地区", ["北京", "上海", "广东", "江苏", "浙江", "其他"])
        company_size = st.selectbox("企业规模", ["微型", "小型", "中型"]) 

    years_in_business = max(0.0, round((date.today() - established_date).days / 365.25, 2))
    st.caption(f"按日历计算的成立年限：约 {years_in_business} 年")

    st.markdown("---")
    st.subheader("核心经营与财务（近一年）")
    col_c, col_d, col_e = st.columns(3)
    with col_c:
        revenue = st.number_input("年营业收入（万元）", min_value=0.0, step=1000.0)
        total_assets = st.number_input("资产总额（万元）", min_value=0.0, step=1000.0)
    with col_d:
        net_profit = st.number_input("净利润（万元）", step=100.0, format="%.2f")
        total_liabilities = st.number_input("负债总额（万元）", min_value=0.0, step=1000.0)
    with col_e:
        op_cash_flow = st.number_input("经营性现金流净额（万元）", step=100.0, format="%.2f")

    st.markdown("---")
    st.subheader("合规与外部信号")
    col_f, col_g, col_h = st.columns(3)
    with col_f:
        overdue_in_12m = st.radio("近12个月是否发生逾期", ["否", "是"], horizontal=True)
    with col_g:
        negative_records = st.radio("是否有处罚/诉讼/失信记录", ["否", "是"], horizontal=True)
    with col_h:
        tax_credit_level = st.selectbox("税务信用等级", ["A", "B", "M", "C", "D"])

    st.markdown("---")
    st.subheader("抵质押与担保")
    col_i, col_j = st.columns(2)
    with col_i:
        collateral_type = st.selectbox("抵押/担保情况", ["无", "抵押", "保证", "混合"]) 
    with col_j:
        collateral_amount = st.number_input(
            "抵质押估值/担保金额（万元）",
            min_value=0.0,
            step=100.0,
            format="%.2f",
            disabled=(collateral_type == "无"),
        )

    submitted = st.form_submit_button("提交并查看汇总")

if 'submitted' in locals() and submitted:
    st.success("数据已提交，以下为汇总与关键指标：")

    # 自动计算指标
    debt_ratio = (total_liabilities / total_assets) if total_assets and total_assets > 0 else None
    net_profit_margin = (net_profit / revenue) if revenue and revenue > 0 else None

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("成立年限（年）", f"{years_in_business}")
    with c2:
        st.metric("资产负债率", f"{debt_ratio:.2%}" if debt_ratio is not None else "-")
    with c3:
        st.metric("净利率", f"{net_profit_margin:.2%}" if net_profit_margin is not None else "-")

    st.divider()
    st.write(
        {
            "统一社会信用代码": credit_code,
            "企业名称": company_name,
            "成立日期": established_date,
            "成立年限（年）": years_in_business,
            "行业类别": industry_category,
            "所在地区": region,
            "企业规模": company_size,
            "年营业收入（万元）": revenue,
            "净利润（万元）": net_profit,
            "资产总额（万元）": total_assets,
            "负债总额（万元）": total_liabilities,
            "经营性现金流净额（万元）": op_cash_flow,
            "近12个月是否发生逾期": overdue_in_12m,
            "是否有处罚/诉讼/失信记录": negative_records,
            "税务信用等级": tax_credit_level,
            "抵押/担保情况": collateral_type,
            "抵质押估值/担保金额（万元）": 0.0 if collateral_type == "无" else collateral_amount,
        }
    )


if st.button("退出系统"):
    st.switch_page("pages/page1.py")
