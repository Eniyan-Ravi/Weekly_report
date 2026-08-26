import logging

LOG_FILE = "data/rejects/reject_log.log"


logging.basicConfig(filename=LOG_FILE,filemode='w',level=logging.WARNING,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def log_rejection(row, reason):
    logging.warning(
        "order_id=" + str(row.get("order_id")) + " | "
        + "customer_id=" + str(row.get("customer_id")) + " | "
        + "product_id=" + str(row.get("product_id")) + " | "
        + "reject_reason=" + str(reason)
    )