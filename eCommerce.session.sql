-- wms_productunitconverter
-- CREATE TABLE IF NOT EXISTS `wms_productunitconverter` (
--                     `id` int(11) NOT NULL AUTO_INCREMENT,
--                     `product_id` int(11) NOT NULL,
--                     `title` varchar(24) NOT NULL,
--                     `conversion_rate` float NOT NULL,
--                     `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
--                     `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
--                     PRIMARY KEY (`id`),
--                     KEY `wms_productunitconverter_product_id_7f3c7f4f_fk_wms_stockinproduct_id` (`product_id`),
--                     CONSTRAINT `wms_productunitconverter_product_id_7f3c7f4f_fk_wms_stockinproduct_id` FOREIGN KEY (`product_id`) REFERENCES `wms_stockinproduct` (`id`)
--                   ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

-- remove rows from wms_mergedproductsinstock
delete from wms_mergedproductsinstock;