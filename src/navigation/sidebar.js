export default [
  {
    title: "dashboard",
    icon: "ChartPieIcon",
    route: "dashboard",
  },
  {
    title: "products",
    icon: "TagIcon",
    children: [
      {
        title: "newProduct",
        route: "new-product",
      },
      {
        title: "productList",
        route: "products",
      },
    ],
  },
  {
    title: "sales",
    icon: "ShoppingCartIcon",
    children: [
      {
        title: "newSale",
        route: "new-sale",
      },
      {
        title: "salesList",
        route: "sales",
      },
    ],
  },
  {
    title: "purchases",
    icon: "BuildingStorefrontIcon",
    children: [
      {
        title: "newPurchase",
        route: "new-purchase",
      },
      {
        title: "purchasesList",
        route: "purchases",
      },
    ],
  },
  {
    title: "users",
    icon: "UserGroupIcon",
    children: [
      {
        title: "newUser",
        route: "new-user",
      },
      {
        title: "usersList",
        route: "users",
      },
    ],
  },
  {
    title: "analytics",
    icon: "ArrowTrendingUpIcon",
    children: [
      {
        title: "products",
        route: "product-analytics",
      },
      {
        title: "sales",
        route: "sale-analytics",
      },
      {
        title: "purchases",
        route: "purchase-analytics",
      },
      {
        title: "users",
        route: "user-analytics",
      },
    ],
  },
];
