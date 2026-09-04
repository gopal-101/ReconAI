import streamlit as st
import pandas as pd

from ai_agent import analyze_case


# -----------------------------
# PAGE SETUP
# -----------------------------

st.set_page_config(
    page_title="ReconAI",
    page_icon="💰",
    layout="wide"
)

st.title("💰 ReconAI")
st.subheader("AI Financial Reconciliation Assistant")

st.write(
    "Upload invoices and payment transactions to find matches "
    "and use AI to review ambiguous cases."
)

st.divider()


# -----------------------------
# FILE UPLOAD
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    st.write("### 📄 Invoices")

    invoice_file = st.file_uploader(
        "Upload invoices CSV",
        type=["csv"]
    )

with col2:
    st.write("### 💳 Transactions")

    transaction_file = st.file_uploader(
        "Upload transactions CSV",
        type=["csv"]
    )


# -----------------------------
# RECONCILIATION
# -----------------------------

if invoice_file is not None and transaction_file is not None:

    invoices = pd.read_csv(invoice_file)
    transactions = pd.read_csv(transaction_file)

    st.success(
        f"Loaded {len(invoices)} invoices and "
        f"{len(transactions)} transactions. ✅"
    )

    st.divider()

    # -------------------------
    # RUN RECONCILIATION
    # -------------------------

    if st.button(
        "🔍 Run AI Reconciliation",
        type="primary",
        use_container_width=True
    ):

        results = []

        exact_matches = 0
        ai_matches = 0
        needs_review = 0

        progress = st.progress(0)

        # -------------------------
        # PROCESS EACH INVOICE
        # -------------------------

        for index, invoice in invoices.iterrows():

            customer = str(invoice["customer"])

            invoice_amount = float(
                invoice["amount"]
            )

            # Find transactions for the same customer
            customer_transactions = transactions[
                transactions["customer"]
                .astype(str)
                .str.lower()
                == customer.lower()
            ].copy()

            # -------------------------
            # NO PAYMENT FOUND
            # -------------------------

            if customer_transactions.empty:

                needs_review += 1

                results.append({
                    "Invoice": invoice["invoice_id"],
                    "Payment": "None",
                    "Invoice Amount": invoice_amount,
                    "Payment Amount": 0,
                    "Difference": invoice_amount,
                    "Status": "Needs Review ❌",
                    "AI Confidence": "",
                    "AI Reason": "No payment found"
                })

                progress.progress(
                    (index + 1) / len(invoices)
                )

                continue

            # -------------------------
            # FIND CLOSEST PAYMENT
            # -------------------------

            customer_transactions["difference"] = (
                customer_transactions["amount"]
                .astype(float)
                - invoice_amount
            ).abs()

            best = customer_transactions.loc[
                customer_transactions["difference"].idxmin()
            ]

            payment_amount = float(
                best["amount"]
            )

            difference = float(
                best["difference"]
            )

            ai_confidence = ""
            ai_reason = ""

            # -------------------------
            # EXACT MATCH
            # -------------------------

            if difference == 0:

                status = "Matched ✅"

                exact_matches += 1

            # -------------------------
            # SMALL DIFFERENCE → GEMINI
            # -------------------------

            elif difference <= 100:

                ai_result = analyze_case(
                    invoice,
                    {
                        "transaction_id":
                            best["transaction_id"],

                        "customer":
                            best["customer"],

                        "amount":
                            best["amount"]
                    }
                )

                ai_confidence = ai_result.get(
                    "confidence",
                    0
                )

                ai_reason = ai_result.get(
                    "reason",
                    ""
                )

                if ai_result.get(
                    "decision"
                ) == "likely_match":

                    status = "AI Match 🤖"

                    ai_matches += 1

                else:

                    status = "AI Review ⚠️"

                    needs_review += 1

            # -------------------------
            # LARGE DIFFERENCE
            # -------------------------

            else:

                status = "Needs Review ❌"

                needs_review += 1

                ai_reason = (
                    "Payment amount differs "
                    "significantly."
                )

            # -------------------------
            # SAVE RESULT
            # -------------------------

            results.append({
                "Invoice": invoice["invoice_id"],
                "Payment": best["transaction_id"],
                "Invoice Amount": invoice_amount,
                "Payment Amount": payment_amount,
                "Difference": difference,
                "Status": status,
                "AI Confidence": ai_confidence,
                "AI Reason": ai_reason
            })

            progress.progress(
                (index + 1) / len(invoices)
            )

        progress.empty()

        results_df = pd.DataFrame(results)

        # -------------------------
        # DASHBOARD
        # -------------------------

        st.divider()

        st.header("📊 Reconciliation Results")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Records",
                len(invoices)
            )

        with col2:
            st.metric(
                "Exact Matches",
                exact_matches
            )

        with col3:
            st.metric(
                "AI Matches",
                ai_matches
            )

        with col4:
            st.metric(
                "Needs Review",
                needs_review
            )

        # -------------------------
        # MAIN RESULTS TABLE
        # -------------------------

        st.divider()

        st.subheader("🔎 Transaction Results")

        # Only show the important transaction
        # information in the main table.
        main_results = results_df[
            [
                "Invoice",
                "Payment",
                "Invoice Amount",
                "Payment Amount",
                "Difference",
                "Status"
            ]
        ]

        st.dataframe(
            main_results,
            use_container_width=True,
            hide_index=True
        )

        # -------------------------
        # AI ANALYSIS DETAILS
        # -------------------------

        st.divider()

        st.subheader("🤖 AI Analysis Details")

        ai_cases = results_df[
            results_df["AI Reason"].astype(str).str.strip() != ""
        ]

        if ai_cases.empty:

            st.info(
                "No AI analysis was required."
            )

        else:

            for _, case in ai_cases.iterrows():

                invoice_id = case["Invoice"]
                payment_id = case["Payment"]
                status = case["Status"]
                confidence = case["AI Confidence"]
                reason = case["AI Reason"]

                with st.expander(
                    f"{invoice_id} → {payment_id} | {status}"
                ):

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(
                            f"**Invoice:** {invoice_id}"
                        )

                        st.write(
                            f"**Payment:** {payment_id}"
                        )

                    with col2:
                        st.write(
                            f"**Status:** {status}"
                        )

                        if confidence != "":
                            st.write(
                                f"**AI Confidence:** "
                                f"{confidence}"
                            )

                    st.write("**AI Reason:**")

                    st.info(
                        str(reason)
                    )

        # -------------------------
        # EXCEPTIONS
        # -------------------------

        st.divider()

        st.subheader("⚠️ Cases Requiring Attention")

        exceptions = results_df[
            results_df["Status"] != "Matched ✅"
        ]

        if exceptions.empty:

            st.success(
                "All transactions were successfully matched! 🎉"
            )

        else:

            exception_table = exceptions[
                [
                    "Invoice",
                    "Payment",
                    "Invoice Amount",
                    "Payment Amount",
                    "Difference",
                    "Status"
                ]
            ]

            st.dataframe(
                exception_table,
                use_container_width=True,
                hide_index=True
            )

        # -------------------------
        # DOWNLOAD
        # -------------------------

        st.divider()

        st.subheader("📥 Report")

        csv_data = results_df.to_csv(
            index=False
        )

        st.download_button(
            "Download Reconciliation Report",
            csv_data,
            "reconai_results.csv",
            "text/csv",
            use_container_width=True
        )

else:

    st.info(
        "Upload both CSV files to start reconciliation."
    )