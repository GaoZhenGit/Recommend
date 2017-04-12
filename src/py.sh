#! /bin/bash
case $1 in
    "database")
    python -m database.database_reader
    ;;

    "lda")
    python -m mylda.runner
    ;;
    
    "lda_executor")
    python -m mylda.lda_executor
    ;;
    
    "lda_filter")
    python -m mylda.lda_filter
    ;;
    
    "mf")
    python -m mf.runner
    ;;
    
    "mf_matrix")
    python -m mf.mf_matrix
    ;;
    
    "mf_mf")
    python -m mf.mf
    ;;
    
    "mf_score")
    python -m mf.mf_score
    ;;
    
    "mf_result")
    python -m mf.mf_result
    ;;

    "mf_fastmf")
    python -m mf.fast_mf
    ;;
    
    "con")
    python -m conclusion.conclusion_cal $2
    ;;
    
    "dir_mf")
    python -m other.dir_mf
    ;;

    "mt")
    python -m other.mosttop
    ;;

    "dir_lda")
    python -m other.dir_lda
    ;;

    "dir_fmf")
    python -m other.dir_fastmf
    ;;

    "mt_pre")
    python -m other.mt_pre $2 $3
    ;;

    "mt_post")
    python -m other.mt_post
    ;;
esac