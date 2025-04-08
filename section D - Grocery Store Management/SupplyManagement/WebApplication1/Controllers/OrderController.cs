using Azure.Core;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using WebApplication1.Models;

namespace WebApplication1.Controllers
{
	[Route("api/[controller]")]
	[ApiController]
	public class OrderController : ControllerBase
	{
		private readonly LocalDatabase _context = new();
		public OrderController(LocalDatabase context)
		{
			_context = context;
		}
		[HttpGet]
		public IActionResult GetAllOrders()
		{
			return Ok(_context.Orders);
		}

		// GET: api/order/{id}
		[HttpGet("{id}")]
		public IActionResult GetOrder(int id)
		{
			var order = _context.Orders.FirstOrDefault(o => o.Id == id);
			if (order == null)
				return NotFound($"Order of id: {id} not found.");
			return Ok(order);
		}

		// POST: api/order
		[HttpPost]
		public IActionResult CreateOrder([FromBody] CreateOrderRequest request)
		{
			Supplier? supplier = _context.Suppliers.FirstOrDefault(s => s.Id == request.SupplierId);
			if (supplier == null)
				return BadRequest("Supplier of the Order doesn't exist.");

			Order newOrder = new()
			{
				Id = _context.Orders.Count + 1,
				SupplierId = request.SupplierId,
				Items = new List<OrderItem>(),
			};

			decimal total = 0;

			foreach (var item in request.Items)
			{
				var product = supplier.Products.FirstOrDefault(p => p.Id == item.ProductId);
				if (product == null)
					return BadRequest($"This supplier doesn't provide the product of ID: {item.ProductId}.");

				if (item.Quantity < product.MinimumQuantity)
					return BadRequest($"Minimum quantity for {product.Name} is {product.MinimumQuantity}.");

				var orderItem = new OrderItem
				{
					Id = _context.Orders.SelectMany(o => o.Items).Count() + 1,
					ProductId = product.Id,
					Quantity = item.Quantity,
					Product = product
				};
				newOrder.Items.Add(orderItem);

				total += item.Quantity * product.PricePerUnit;
			}

			newOrder.TotalAmount = total;

			_context.Orders.Add(newOrder);
			return CreatedAtAction(nameof(GetOrder), new { id = newOrder.Id }, newOrder);
		}

		// PUT: api/order/{id}/confirmdelivery/
		[HttpPut("{id}/confirmdelivery")]
		public IActionResult ConfirmOrderDelivery(int id)
		{
			var existingOrder = _context.Orders.FirstOrDefault(o => o.Id == id);
			if (existingOrder == null)
				return NotFound($"Order of id: {id} not found.");

			Supplier? supplier = _context.Suppliers.FirstOrDefault(s => s.Id == existingOrder.SupplierId);
			if (supplier == null)
				return BadRequest("Supplier of the Order doesn't exist.");

			string name = supplier.ContactPerson;
			string number = supplier.PhoneNumber;

			if (existingOrder.Status == OrderStatus.Pending)
				return BadRequest($"Order is yet to be sent. Phone {name} on {number} and tell them to get a move on.");

			if (existingOrder.Status == OrderStatus.Delivered)
				return BadRequest("Order is already delivered.");

			existingOrder.Status = OrderStatus.Delivered;
			existingOrder.CompletedAt = DateTime.Now;

			return Ok(existingOrder);
		}
	}

	public class CreateOrderRequest
	{
		public int SupplierId { get; set; }
		public List<OrderItemRequest> Items { get; set; } = new();
	}

	public class OrderItemRequest
	{
		public int ProductId { get; set; }
		public int Quantity { get; set; }
	}

}
