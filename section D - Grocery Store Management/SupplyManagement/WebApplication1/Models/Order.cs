namespace WebApplication1.Models
{
	public enum OrderStatus
	{
		Pending,
		InProgress,
		Delivered,
	}
	public class Order
	{
		public int Id { get; set; }
		public int SupplierId { get; set; }
		public DateTime CreatedAt { get; set; }
		public DateTime CompletedAt { get; set; }
		public decimal TotalAmount { get; set; }
		public OrderStatus Status { get; set; }
		public List<OrderItem> Items { get; set; } = new();
		public Order()
		{
			CreatedAt = DateTime.Now;
			Status = OrderStatus.Pending;
		}
	}
}
