-- start query 1 in stream 0 using template query8.tpl
select  s_store_name
      ,sum(ss_net_profit)
 from store_sales
     ,date_dim
     ,store,
     (select ca_zip
     from (
      SELECT substr(ca_zip,1,5) ca_zip
      FROM customer_address
      WHERE substr(ca_zip,1,5) IN (
                          '42416','11821','29026','18697','54532','36912',
                          '29570','19750','55872','62699','63334',
                          '62362','23232','24357','46143','12598',
                          '37395','27237','98550','61143','12229',
                          '24457','15713','51057','43163','17798',
                          '30934','63597','16172','82144','25389',
                          '23566','37310','90273','76773','67215',
                          '44688','44706','88658','19420','10230',
                          '94699','21730','27283','25991','56807',
                          '60655','44509','17507','90777','21298',
                          '70747','98501','34064','57016','79066',
                          '36899','90791','57921','33227','71309',
                          '68255','63621','64395','41563','73807',
                          '60671','57121','73509','21540','24166',
                          '96372','86336','40933','15693','85580',
                          '41745','83075','39826','19237','50983',
                          '37948','27123','14798','45147','66439',
                          '41631','58496','31159','81233','34091',
                          '42321','36775','28640','91282','36650',
                          '40629','32828','32475','30865','19191',
                          '37609','87703','79614','29046','47632',
                          '66531','11757','62557','24890','34989',
                          '53049','64664','57964','74765','23675',
                          '33393','78634','40071','95717','42911',
                          '38403','18454','32218','53949','49947',
                          '41439','14084','23281','80601','71609',
                          '65323','27106','10481','61463','16540',
                          '61886','28454','85040','60460','19837',
                          '18981','23956','22332','19102','74789',
                          '53551','99465','60394','49250','88827',
                          '25747','93835','69554','38848','14955',
                          '22345','22687','25148','12760','15483',
                          '44435','57557','29439','81842','20674',
                          '24446','43385','52959','50176','50951',
                          '38531','29597','77660','19074','51276',
                          '60170','60716','95708','70163','29876',
                          '60131','73899','18471','88928','72747',
                          '88970','10922','72647','18847','21037',
                          '41786','34405','21086','95461','58863',
                          '10210','34674','22172','19981','99861',
                          '30710','92195','39667','10126','12739',
                          '26902','18936','90802','22478','23799',
                          '25352','27239','11071','81434','41155',
                          '13931','59816','98432','68581','91633',
                          '75828','69082','87533','67396','23173',
                          '56896','57103','51260','65979','59978',
                          '34021','22774','12114','29935','71113',
                          '48396','61935','60227','63915','69668',
                          '46060','17502','54745','32249','33634',
                          '63514','83549','14305','79820','23391',
                          '31032','16852','12110','55475','46974',
                          '75061','80749','16359','53013','18689',
                          '23023','95057','40944','97046','31018',
                          '54920','42842','41266','73130','76360',
                          '27167','45532','77306','56747','54846',
                          '14044','70983','75646','94250','42803',
                          '82006','68393','35921','17117','59158',
                          '52513','12421','44318','91437','23589',
                          '54651','17974','29049','23915','75336',
                          '28031','14582','84580','77319','46219',
                          '26975','14439','46943','19457','13684',
                          '59624','92817','94615','48447','44265',
                          '38929','36149','70795','82768','46299',
                          '54172','62884','84734','24902','83841',
                          '98219','90534','34317','82911','73863',
                          '55263','24506','13662','13410','69041',
                          '40396','74111','32154','62033','55812',
                          '94083','48392','19792','52053','27270',
                          '29742','59306','21822','25429','13471',
                          '28095','64389','82133','50118','58986',
                          '22468','96466','40512','26965','22494',
                          '11974','83958','57017','33740','79544',
                          '30683','79830','22796','96380','77106',
                          '58573','50573','36161','32452','35337',
                          '18514','51772','37622','52363','32850',
                          '11289','88521','98998','64028','37033',
                          '18600','61316','73273','78039','87052',
                          '95154','80094','22203','51704','38416',
                          '36922','55647','47564','92250','19591',
                          '60326','88657','90324','80423')
     intersect
      select ca_zip
      from (SELECT substr(ca_zip,1,5) ca_zip,count(*) cnt
            FROM customer_address, customer
            WHERE ca_address_sk = c_current_addr_sk and
                  c_preferred_cust_flag='Y'
            group by ca_zip
            having count(*) > 10)A1)A2) V1
 where ss_store_sk = s_store_sk
  and ss_sold_date_sk = d_date_sk
  and d_qoy = 1 and d_year = 2002
  and (substr(s_zip,1,2) = substr(V1.ca_zip,1,2))
 group by s_store_name
 order by s_store_name
 limit 100;

-- end query 1 in stream 0 using template query8.tpl
