using Microsoft.EntityFrameworkCore;

namespace WebApplication1.Models
{
	public class SuppliersContext : DbContext
	{
		public DbSet<Supplier> Suppliers { get; set; }
		public DbSet<Product> Products { get; set; }
		public DbSet<Order> Orders { get; set; }
		public DbSet<OrderItem> OrderItems { get; set; }

		public SuppliersContext(DbContextOptions<SuppliersContext> options) : base(options) { }

	}
}
