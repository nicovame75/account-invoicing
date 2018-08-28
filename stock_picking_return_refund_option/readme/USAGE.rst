To use this module, when some customer returns some refundable products to you
after you created an invoice, you need to:

For a sale order:

#. Go to *Sales > Sales Orders > Create*.
#. Choose a customer and add a product whose *Invoicing Policy* is *Delivered
   quantities*, and input some quantity to sell.
#. Confirm the sale.
#. Go to *Delivery > Validate > Apply*.
#. Return to the sale order.
#. Press *Create Invoice > Invoiceable lines > Create and View Invoices*.
#. The created invoice's amount is the same you sold.
#. Return to the sale order.
#. Go to *Delivery > Reverse*.
#. Set *Quantity* to a lower quantity than the sold one, and enable
   *To Refund*.
#. Press *Return > Validate > Apply*.
#. Return to the sale order.
#. Press *Create Invoice > Invoiceable lines (deduct down payments) >
   Create and View Invoices*.
#. A refund is created for the quantity you returned before.

For allowing to refund quantities after the picking has been confirmed if you
did not check 'to refund' in wizard, you can change the value
of 'Refund Options' field.
