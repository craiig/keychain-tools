-- start query 1 in stream 0 using template query28.tpl
select  *
from (select avg(ss_list_price) B1_LP
            ,count(ss_list_price) B1_CNT
            ,count(distinct ss_list_price) B1_CNTD
      from store_sales
      where ss_quantity between 0 and 5
        and (ss_list_price between 7 and 7+10 
             or ss_coupon_amt between 1469 and 1469+1000
             or ss_wholesale_cost between 69 and 69+20)) B1,
     (select avg(ss_list_price) B2_LP
            ,count(ss_list_price) B2_CNT
            ,count(distinct ss_list_price) B2_CNTD
      from store_sales
      where ss_quantity between 6 and 10
        and (ss_list_price between 36 and 36+10
          or ss_coupon_amt between 3051 and 3051+1000
          or ss_wholesale_cost between 16 and 16+20)) B2,
     (select avg(ss_list_price) B3_LP
            ,count(ss_list_price) B3_CNT
            ,count(distinct ss_list_price) B3_CNTD
      from store_sales
      where ss_quantity between 11 and 15
        and (ss_list_price between 84 and 84+10
          or ss_coupon_amt between 1562 and 1562+1000
          or ss_wholesale_cost between 48 and 48+20)) B3,
     (select avg(ss_list_price) B4_LP
            ,count(ss_list_price) B4_CNT
            ,count(distinct ss_list_price) B4_CNTD
      from store_sales
      where ss_quantity between 16 and 20
        and (ss_list_price between 19 and 19+10
          or ss_coupon_amt between 4397 and 4397+1000
          or ss_wholesale_cost between 39 and 39+20)) B4,
     (select avg(ss_list_price) B5_LP
            ,count(ss_list_price) B5_CNT
            ,count(distinct ss_list_price) B5_CNTD
      from store_sales
      where ss_quantity between 21 and 25
        and (ss_list_price between 131 and 131+10
          or ss_coupon_amt between 7442 and 7442+1000
          or ss_wholesale_cost between 27 and 27+20)) B5,
     (select avg(ss_list_price) B6_LP
            ,count(ss_list_price) B6_CNT
            ,count(distinct ss_list_price) B6_CNTD
      from store_sales
      where ss_quantity between 26 and 30
        and (ss_list_price between 102 and 102+10
          or ss_coupon_amt between 17781 and 17781+1000
          or ss_wholesale_cost between 46 and 46+20)) B6
limit 100;

-- end query 1 in stream 0 using template query28.tpl
