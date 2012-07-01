CREATE DATABASE queue;
use queue;

CREATE TABLE IF NOT EXISTS queue_list
(
  qId int(10) NOT NULL AUTO_INCREMENT,
  userid int(10) NOT NULL,
  ip_address varchar(15) NOT NULL,
  subscription_level int,
  scan_options varchar(500),
  scan_running TINYINT(1), 
  CONSTRAINT pk_queue_qId PRIMARY KEY (qId)
);

commit;

INSERT INTO queue_list
(userid, ip_address, subscription_level, scan_options)
VALUES
(000001, '172.25.25.50', 1, '-sT -sV -O -P0');

commit;

GRANT USAGE on *.* to aivscan@localhost identified by 'Fish dont fry in the kitchen.';
GRANT ALL PRIVILEGES on queue.* to aivscan@localhost;
COMMIT;

