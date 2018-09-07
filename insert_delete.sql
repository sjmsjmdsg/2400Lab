do
$$
DECLARE
	counter INTEGER := 0;
	pri_key VARCHAR := '0';
	letter VARCHAR := 'A';
BEGIN

	LOOP
	EXIT WHEN counter = 100000;
		counter := counter + 1;
		INSERT INTO basics VALUES(pri_key, CONCAT('tvEpisode', pri_key), '', '', false, 0, '', '130', CONCAT('{', 'Action', ',', 'Adventure', ',', 'Animation', ',',  letter, '}') :: VARCHAR[]);
		pri_key := CAST(CAST(pri_key AS INTEGER) + 1 AS VARCHAR);
		letter := CHR(counter % 26 + 65);
	END LOOP;
	
	counter := 0;
	pri_key := '0';
	
	LOOP
	EXIT WHEN counter = 100000;
		counter := counter + 1;
		DELETE FROM basics WHERE tconst = pri_key;
		pri_key := CAST(CAST(pri_key AS INTEGER) + 1 AS VARCHAR);
	END LOOP;

END;
$$;