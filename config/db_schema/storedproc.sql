USE aivs;

DROP PROCEDURE IF EXISTS pInsertScan;

DELIMITER |
CREATE PROCEDURE pInsertScan(
								IN v_userid INT, 
								IN v_version TEXT, 
								IN v_args TEXT, 
								IN v_startstr TEXT,
								IN v_endstr TEXT
							)
BEGIN
   INSERT INTO scans (
						userId, 
						version, 
						args, 
						startstr, 
						endstr
					) 
			values 	(
						v_userid, 
						v_version, 
						v_args, 
						v_startstr, 
						v_endstr
					); 
	SELECT @@identity;
END
|

DROP PROCEDURE IF EXISTS pInsertHost;
CREATE PROCEDURE pInsertHost(
								IN v_sid INT,
								IN v_ip4 TEXT, 
								IN v_hostname TEXT, 
								IN v_status TEXT, 
								IN v_mac TEXT, 
								IN v_vendor TEXT,
								IN v_ip6 TEXT, 
								IN v_distance INT, 
								IN v_uptime TEXT,
								IN v_upstr TEXT
							)
BEGIN
	INSERT INTO hosts 	(
							sid,
							ip4, 
							hostname,
							status,
							mac,
							vendor,
							ip6, 
							distance, 
							uptime,
							upstr
						)
				VALUES	(
							v_sid,
							v_ip4, 
							v_hostname, 
							v_status, 
							v_mac, 
							v_vendor,
							v_ip6, 
							v_distance, 
							v_uptime,
							v_upstr
						);
	SELECT @@identity;
END
|
							
DROP PROCEDURE IF EXISTS pInsertOS;
CREATE PROCEDURE pInsertOS (
										IN v_hid INT,
										IN v_name TEXT,
										IN v_family TEXT,
										IN v_generation TEXT,
										IN v_type TEXT,
										IN v_vendor TEXT,
										IN v_accuracy INT
							)
BEGIN
	INSERT INTO os 	(
						hid,
						name,
						family,
						generation,
						type,
						vendor,
						accuracy
					)
			VALUES	(
						v_hid,
						v_name,
						v_family,
						v_generation,
						v_type,
						v_vendor,
						v_accuracy
					);
END
|

DROP PROCEDURE IF EXISTS pInsertPort;
CREATE PROCEDURE pInsertPort	(
									IN v_hid INT,
									IN v_port INT, 
									IN v_state TEXT,
									IN v_name TEXT,
									IN v_product TEXT,
									IN v_version TEXT,
									IN v_fingerprint TEXT,
									IN v_proto TEXT
								)
BEGIN
	INSERT INTO ports 	(
							hid,
							port,
							state,
							name,
							product,
							version,
							fingerprint,
							proto
						)
			VALUES		(
							v_hid,
							v_port, 
							v_state,
							v_name,
							v_product,
							v_version,
							v_fingerprint,
							v_proto
						);
END
|

DROP PROCEDURE IF EXISTS pInsertVuln;
CREATE PROCEDURE pInsertVuln (
										IN v_hid INT,
										IN v_tvid INT
										)
BEGIN
	INSERT INTO vulns	(
							hid,
							tvid
						)
			VALUES		(
							v_hid,
							v_tvid
						);
END
|

DROP PROCEDURE IF EXISTS pGetTextVulnRef_byScriptID;
CREATE PROCEDURE pGetTextVulnRef_byScriptID	(
									IN v_scriptID VARCHAR(100)
								)
BEGIN
	SELECT							tvid,
									ScriptID,
									MatchString,
									VulnString,
									FixString
	FROM TextVulns
	WHERE ScriptID = v_scriptID;
END
|

DELIMITER ; 
	    
