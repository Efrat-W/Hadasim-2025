using Microsoft.AspNetCore.Identity.Data;
using Microsoft.AspNetCore.Mvc;
using WebApplication1.Models;

namespace WebApplication1.Controllers
{
	[Route("api/[controller]")]
	[ApiController]
	public class SupplierController : ControllerBase
	{
		private readonly LocalDatabase _context = new();
		public SupplierController(LocalDatabase context)
		{
			_context = context;
		}

		[HttpGet]
		public IActionResult GetAllSuppliers()
		{
			return Ok(_context.Suppliers);
		}

		//// GET: api/supplier/{id}
		//[HttpGet("{id}")]
		//public IActionResult GetSupplier(int id)
		//{
		//	var supplier = _context.Suppliers.FirstOrDefault(s => s.Id == id);
		//	if (supplier == null)
		//		return NotFound($"Supplier of id: {id} not found.");
		//	return Ok(supplier);
		//}

		// POST: api/supplier
		[HttpPost]
		public IActionResult CreateSupplier([FromBody] Supplier newSupplier)
		{
			newSupplier.Id = _context.Suppliers.Count + 1;

			_context.Suppliers.Add(newSupplier);
			return Created($"api/supplier/{newSupplier.Id}", newSupplier);
		}

		// POST: api/supplier/login
		[HttpPost("login")]
		public IActionResult Login([FromBody] LoginRequest request)
		{
			var supplier = _context.Suppliers.FirstOrDefault(s =>
				s.CompanyName == request.CompanyName &&
				s.ContactPerson == request.ContactPerson &&
				s.Password == request.Password);

			if (supplier == null)
				return BadRequest("Incorrect login info. Don't have an account? Sign up!");

			LoggedInUser.CurrentSupplier = supplier;
			return Ok(supplier);
		}


		// GET: api/supplier/{supplierId}/orders
		[HttpGet("{supplierId}/orders")]
		public IActionResult GetOrdersForSupplier(int supplierId)
		{
			if (LoggedInUser.CurrentSupplier == null)
				return Unauthorized("Please log in first.");
			var orders = _context.Orders.Where(o => o.SupplierId == supplierId).ToList();
			if (orders == null || orders.Count == 0)
				return NotFound($"No orders found for supplier of ID: {supplierId}");
			return Ok(orders);
		}

		// PUT: api/supplier/order/{orderId}/confirm?{supplierId}
		[HttpPut("order/{orderId}/confirm")]
		public IActionResult ConfirmOrder(int supplierId, int orderId)
		{
			if (LoggedInUser.CurrentSupplier == null)
				return Unauthorized("Please log in first.");
			var order = _context.Orders.FirstOrDefault(o => o.Id == orderId && o.SupplierId == supplierId);
			if (order == null)
				return NotFound($"Order of ID: {orderId} not found.");

			if (order.Status != OrderStatus.Pending)
				return BadRequest("Only Pending orders can be confirmed.");

			order.Status = OrderStatus.InProgress;
			return Ok(order);
		}


	}

	public class LoginRequest
	{
		public string CompanyName { get; set; }
		public string ContactPerson { get; set; }
		public string Password { get; set; }

	}
}
 