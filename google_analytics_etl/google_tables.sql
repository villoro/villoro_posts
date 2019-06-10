# ---------------- CAMPAIGNS GOOGLE ------------------

DROP TABLE IF EXISTS campaigns_google;
CREATE TABLE campaigns_google (
    `date` DATE NULL DEFAULT NULL,
    `campaign_id` VARCHAR(255) NULL DEFAULT NULL,
    `campaign` VARCHAR(255) NULL DEFAULT NULL,
    `product` VARCHAR(255) NULL DEFAULT NULL,

    `users` INT(22) NULL DEFAULT NULL,
    `clicks` INT(22) NULL DEFAULT NULL,
    `cost` DECIMAL(9,3) NULL DEFAULT NULL,
    `impressions` INT(22) NULL DEFAULT NULL,
    `income` DECIMAL(10,3) NULL DEFAULT NULL,
    `orders` DECIMAL(7,3) NULL DEFAULT NULL
) COLLATE='utf8_general_ci';



# ---------------- TRAFFIC ------------------

DROP TABLE IF EXISTS traffic_google;
CREATE TABLE traffic_google (
    `date` DATE NULL DEFAULT NULL,
    `device` VARCHAR(255) NULL DEFAULT NULL,

    `users` INT(22) NULL DEFAULT NULL,
    `sessions` INT(22) NULL DEFAULT NULL,
    `bounce_rate` DECIMAL(7,3) NULL DEFAULT NULL
) COLLATE='utf8_general_ci';
