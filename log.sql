-- Keep a log of any SQL queries you execute as you solve the mystery.

--
-- view crime_scene_reports
--
SELECT *
FROM   crime_scene_reports
WHERE  street LIKE 'Chamberlin Street'
       AND description LIKE '%duck%';

-- id | year | month | day | street | description
-- 295 | 2020 | 7 | 28 | Chamberlin Street | Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse. Interviews were conducted today with three witnesses who were present at the time — each of their interview transcripts mentions the courthouse.

--
-- view interviews
--
SELECT *
FROM   interviews
WHERE  year = 2020
       AND month = 7
       AND day = 28
       AND transcript LIKE '%courthouse%';

-- id | name | year | month | day | transcript
-- 161 | Ruth | 2020 | 7 | 28 | Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away. If you have security footage from the courthouse parking lot, you might want to look for cars that left the parking lot in that time frame.
-- 162 | Eugene | 2020 | 7 | 28 | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at the courthouse, I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money.
-- 163 | Raymond | 2020 | 7 | 28 | As the thief was leaving the courthouse, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.


--
-- courthose parking lot security footage
-- get people that left the parking lot
--
SELECT p.*
FROM   people p
WHERE  license_plate IN (SELECT c.license_plate
                         FROM   courthouse_security_logs c
                         WHERE  c.activity LIKE 'exit'
                                AND c.year = 2020
                                AND c.month = 7
                                AND c.day = 28
                                AND c.hour = 10
                                AND c.minute >= 15
                                AND c.minute <= 25);

-- id | name | phone_number | passport_number | license_plate
-- 221103 | Patrick | (725) 555-4692 | 2963008352 | 5P2BI95
-- 243696 | Amber | (301) 555-4174 | 7526138472 | 6P58WS2
-- 396669 | Elizabeth | (829) 555-5269 | 7049073643 | L93JTIZ
-- 398010 | Roger | (130) 555-0289 | 1695452385 | G412CB7
-- 467400 | Danielle | (389) 555-5198 | 8496433585 | 4328GD8
-- 514354 | Russell | (770) 555-1861 | 3592750733 | 322W7JE
-- 560886 | Evelyn | (499) 555-9472 | 8294398571 | 0NTHK55
-- 686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X


--
-- ATM on Fifer Street withdrawing money
--
SELECT p.*
FROM   people p
WHERE  p.id IN (SELECT b.person_id
                FROM   bank_accounts b
                WHERE  account_number IN (SELECT a.account_number
                                          FROM   atm_transactions a
                                          WHERE
                       a.transaction_type LIKE 'withdraw'
                       AND atm_location LIKE 'Fifer Street'
                       AND a.year = 2020
                       AND a.month = 7
                       AND a.day = 28));

-- id | name | phone_number | passport_number | license_plate
-- 395717 | Bobby | (826) 555-1652 | 9878712108 | 30G67EN
-- 396669 | Elizabeth | (829) 555-5269 | 7049073643 | L93JTIZ
-- 438727 | Victoria | (338) 555-6650 | 9586786673 | 8X428L0
-- 449774 | Madison | (286) 555-6063 | 1988161715 | 1106N58
-- 458378 | Roy | (122) 555-4581 | 4408372428 | QX4YZN3
-- 467400 | Danielle | (389) 555-5198 | 8496433585 | 4328GD8
-- 514354 | Russell | (770) 555-1861 | 3592750733 | 322W7JE
-- 686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X



--
-- thief leaving courthouse, called someone who talked to them for less than a minute
-- caller
--
SELECT p.*
FROM   people p
WHERE  p.phone_number IN (SELECT ph.caller
                          FROM   phone_calls ph
                          WHERE  ph.duration < 60
                                 AND ph.year = 2020
                                 AND ph.month = 7
                                 AND ph.day = 28);

-- id | name | phone_number | passport_number | license_plate
-- 395717 | Bobby | (826) 555-1652 | 9878712108 | 30G67EN
-- 398010 | Roger | (130) 555-0289 | 1695452385 | G412CB7
-- 438727 | Victoria | (338) 555-6650 | 9586786673 | 8X428L0
-- 449774 | Madison | (286) 555-6063 | 1988161715 | 1106N58
-- 514354 | Russell | (770) 555-1861 | 3592750733 | 322W7JE
-- 560886 | Evelyn | (499) 555-9472 | 8294398571 | 0NTHK55
-- 686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X
-- 907148 | Kimberly | (031) 555-6622 | 9628244268 | Q12B3Z3



--
-- earliest flight out of Fiftyville tomorrow
-- passengers
--
SELECT p.*
FROM   people p
WHERE  passport_number IN (SELECT pgr.passport_number
                           FROM   passengers pgr
                           WHERE  pgr.flight_id IN (SELECT f.id
                                                    FROM   flights f
                                                    WHERE
                                  origin_airport_id IN (SELECT
                                  air.id
                                                        FROM
                                  airports air
                                                        WHERE
                                  air.city LIKE 'Fiftyville'
                                                       )
                                  AND f.year = 2020
                                  AND f.month = 7
                                  AND f.day = 29
                                                    ORDER  BY hour,
                                                              minute
                                                    LIMIT  1));


-- id | name | phone_number | passport_number | license_plate
-- 395717 | Bobby | (826) 555-1652 | 9878712108 | 30G67EN
-- 398010 | Roger | (130) 555-0289 | 1695452385 | G412CB7
-- 449774 | Madison | (286) 555-6063 | 1988161715 | 1106N58
-- 467400 | Danielle | (389) 555-5198 | 8496433585 | 4328GD8
-- 560886 | Evelyn | (499) 555-9472 | 8294398571 | 0NTHK55
-- 651714 | Edward | (328) 555-1152 | 1540955065 | 130LD9Z
-- 686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X
-- 953679 | Doris | (066) 555-9701 | 7214083635 | M51FA04


--
-- earliest flight out of Fiftyville tomorrow
-- destination
--
SELECT f.*,
       air_dest.full_name,
       air_dest.city
FROM   flights f
       LEFT JOIN airports air_dest
              ON f.destination_airport_id = air_dest.id
WHERE  origin_airport_id IN (SELECT air.id
                             FROM   airports air
                             WHERE  air.city LIKE 'Fiftyville')
       AND f.year = 2020
       AND f.month = 7
       AND f.day = 29
ORDER  BY hour,
          minute
LIMIT  1;

-- id | origin_airport_id | destination_airport_id | year | month | day | hour | minute | full_name | city
-- 36 | 8 | 4 | 2020 | 7 | 29 | 8 | 20 | Heathrow Airport | London


--
-- thief leaving courthouse, called someone who talked to them for less than a minute
-- receiver
--
SELECT p.*
FROM   people p
WHERE  p.phone_number IN (SELECT ph.receiver
                          FROM   phone_calls ph
                          WHERE  caller LIKE '%(367) 555-5533%'
                                 AND ph.duration < 60
                                 AND ph.year = 2020
                                 AND ph.month = 7
                                 AND ph.day = 28);

-- id | name | phone_number | passport_number | license_plate
-- 864400 | Berthold | (375) 555-8161 |  | 4V16VO0


