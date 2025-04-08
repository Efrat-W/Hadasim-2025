namespace WebApplication1.Models
{
	public class LocalDatabase
	{
		public List<Supplier> Suppliers { get; set; } = new();
		public List<Product> Products { get; set; } = new();
		public List<Order> Orders { get; set; } = new();
	}
}
