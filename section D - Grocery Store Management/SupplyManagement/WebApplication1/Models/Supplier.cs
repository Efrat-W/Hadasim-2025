
namespace WebApplication1.Models
{
	public class Supplier
	{
		public int Id { get; set; }
		public string CompanyName { get; set; }
		public string PhoneNumber { get; set; }
		public string ContactPerson { get; set; }
		public string Password { get; set; }

		public List<Product> Products { get; set; } = new();
	}

	public static class LoggedInUser
	{
		public static Supplier? CurrentSupplier { get; set; }
	}
}