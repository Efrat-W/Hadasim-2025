namespace WebApplication1.Models
{
	public class Product
	{
		public int Id { get; set; }
		public string Name { get; set; }
		public decimal PricePerUnit { get; set; }
		public int MinimumQuantity { get; set; }
	}
}