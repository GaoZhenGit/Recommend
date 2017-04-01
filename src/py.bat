@echo off
if %1 == database python -m database.database_reader
if %1 == lda python -m mylda.runner
if %1 == lda_executor python -m mylda.lda_executor
if %1 == lda_filter python -m mylda.lda_filter

if %1 == mf python -m mf.runner
if %1 == mf_matrix python -m mf.mf_matrix
if %1 == mf_mf python -m mf.mf
if %1 == mf_score python -m mf.mf_score
if %1 == mf_result python -m mf.mf_result

if %1 == con python -m conclusion.conclusion_cal %2

if %1 == dir_mf python -m other.dir_mf
if %1 == mt python -m other.mosttop
if %1 == dir_lda python -m other.dir_lda
if %1 == mt_pre python -m other.mt_pre %2 %3
if %1 == mt_post python -m other.mt_post