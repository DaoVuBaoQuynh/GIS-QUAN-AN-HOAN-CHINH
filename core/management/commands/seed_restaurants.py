import random
from django.core.management.base import BaseCommand
from core.models import Category, Restaurant, DiningTable


class Command(BaseCommand):
    help = "Tạo 50 quán ăn mẫu + bàn thường/VIP"

    def handle(self, *args, **kwargs):
        categories = [
            "Cafe",
            "Buffet",
            "Bún/Mì",
            "Thức ăn nhanh",
            "Lẩu/Nướng",
        ]

        category_objs = {}
        for name in categories:
            obj, _ = Category.objects.get_or_create(name=name)
            category_objs[name] = obj

        names = [
            "Highlands Coffee", "The Coffee House", "KFC", "Lotteria", "Phúc Long",
            "Bún Bò Cô Ba", "Buffet Hải Sản", "Lẩu Nướng Seoul", "Mì Cay 7 Cấp Độ", "Gà Rán 79",
            "Cafe Góc Phố", "Trà Sữa Mây", "Buffet Hoàng Gia", "Bún Riêu Cô Tư", "Phở 24",
            "Bếp Nhà", "Nem Nướng Nha Trang", "Bún Đậu Mắm Tôm", "BBQ Garden", "Sushi Mini",
            "Cafe Sân Vườn", "Pizza Hub", "Burger House", "Lẩu Thái Tomyum", "Cơm Tấm Sài Gòn",
            "Mì Quảng Xưa", "Bánh Canh Cua", "Buffet Nướng Mộc", "Cafe Chill", "Cơm Gà Hội An",
            "Bún Chả Hà Nội", "Cà Phê Mộc", "Bún Cá Nha Trang", "Trà Chanh 1975", "Lẩu Bò 88",
            "Mì Trộn Hàn Quốc", "Bánh Mì Chảo", "Hủ Tiếu Nam Vang", "Cafe Vintage", "Bò Né 3 Ngon",
            "Cơm Niêu", "Lẩu Gà Lá É", "Bún Thái", "Trà Sữa Matcha", "Bánh Xèo Miền Tây",
            "Bún Mắm", "Cafe Rooftop", "Buffet Chay", "Mì Vịt Tiềm", "Nhà Hàng Hoa Sen"
        ]

        streets = [
            "Nguyễn Gia Trí", "Điện Biên Phủ", "Xô Viết Nghệ Tĩnh", "Phan Văn Trị",
            "Lê Quang Định", "Ung Văn Khiêm", "Nguyễn Hữu Cảnh", "Bạch Đằng",
            "Phạm Văn Đồng", "D2 Bình Thạnh"
        ]

        center_lat = 10.8015
        center_lng = 106.7110

        created_restaurants = 0
        created_tables = 0

        for i in range(50):
            name = f"{names[i]} #{i+1}"
            address = f"{random.randint(10, 300)} {random.choice(streets)}, Bình Thạnh, TP.HCM"

            if "Cafe" in name or "Coffee" in name or "Phúc Long" in name:
                cat = category_objs["Cafe"]
            elif "Buffet" in name:
                cat = category_objs["Buffet"]
            elif "Bún" in name or "Mì" in name or "Phở" in name or "Hủ Tiếu" in name:
                cat = category_objs["Bún/Mì"]
            elif "KFC" in name or "Lotteria" in name or "Burger" in name or "Pizza" in name:
                cat = category_objs["Thức ăn nhanh"]
            else:
                cat = category_objs["Lẩu/Nướng"]

            lat = center_lat + random.uniform(-0.018, 0.018)
            lng = center_lng + random.uniform(-0.018, 0.018)

            restaurant, created = Restaurant.objects.get_or_create(
name=name,
                defaults={
                    "address": address,
                    "phone": f"090{random.randint(1000000, 9999999)}",
                    "description": f"{name} - quán ăn mẫu cho đồ án GIS.",
                    "latitude": lat,
                    "longitude": lng,
                    "category": cat,
                    "price_level": random.randint(1, 5),
                    "is_active": True,
                    "image_url": f"https://picsum.photos/seed/quan{i+1}/600/400"
                }
            )

            if created:
                created_restaurants += 1
            else:
                # nếu quán đã tồn tại thì cập nhật thêm cho đủ dữ liệu mới
                restaurant.address = address
                restaurant.phone = f"090{random.randint(1000000, 9999999)}"
                restaurant.description = f"{name} - quán ăn mẫu cho đồ án GIS."
                restaurant.latitude = lat
                restaurant.longitude = lng
                restaurant.category = cat
                restaurant.price_level = random.randint(1, 5)
                restaurant.is_active = True
                restaurant.image_url = f"https://picsum.photos/seed/quan{i+1}/600/400"
                restaurant.save()

            # tạo bàn an toàn, không bị trùng
            table_specs = [
                ("B01", random.choice([2, 4, 6]), "normal", random.choice(["available", "available", "reserved"])),
                ("B02", random.choice([2, 4, 6]), "normal", random.choice(["available", "available", "reserved"])),
                ("B03", random.choice([2, 4, 6]), "normal", random.choice(["available", "available", "reserved"])),
                ("VIP01", random.choice([4, 6, 8]), "vip", random.choice(["available", "reserved"])),
            ]

            for code, capacity, table_type, status in table_specs:
                table, table_created = DiningTable.objects.get_or_create(
                    restaurant=restaurant,
                    code=code,
                    defaults={
                        "capacity": capacity,
                        "table_type": table_type,
                        "status": status,
                    }
                )

                if not table_created:
                    table.capacity = capacity
                    table.table_type = table_type
                    table.status = status
                    table.save()
                else:
                    created_tables += 1

        self.stdout.write(self.style.SUCCESS(
            f"Xong: tạo mới {created_restaurants} quán, {created_tables} bàn."
        ))
