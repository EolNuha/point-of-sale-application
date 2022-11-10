export default [
  {
    title: "dashboard",
    icon: "ChartPieIcon",
    route: "dashboard",
    action: "read",
    subject: "dashboard",
  },
  {
    title: "products",
    icon: "TagIcon",
    action: "read",
    subject: "products",
    children: [
      {
        title: "newProduct",
        route: "new-product",
        action: "write",
        subject: "products",
      },
      {
        title: "productList",
        route: "products",
        action: "read",
        subject: "products",
      },
    ],
  },
  {
    title: "sales",
    icon: "ShoppingCartIcon",
    action: "read",
    subject: "sales",
    children: [
      {
        title: "newSale",
        route: "new-sale",
        action: "write",
        subject: "sales",
      },
      {
        title: "salesList",
        route: "sales",
        action: "read",
        subject: "sales",
      },
    ],
  },
  {
    title: "purchases",
    icon: "BuildingStorefrontIcon",
    action: "read",
    subject: "purchases",
    children: [
      {
        title: "newPurchase",
        route: "new-purchase",
        action: "write",
        subject: "purchases",
      },
      {
        title: "purchasesList",
        route: "purchases",
        action: "read",
        subject: "purchases",
      },
    ],
  },
  {
    title: "users",
    icon: "UserGroupIcon",
    action: "read",
    subject: "users",
    children: [
      {
        title: "newUser",
        route: "new-user",
        action: "write",
        subject: "users",
      },
      {
        title: "usersList",
        route: "users",
        action: "read",
        subject: "users",
      },
    ],
  },
  {
    title: "analytics",
    icon: "ArrowTrendingUpIcon",
    action: "read",
    subject: "analytics",
    children: [
      {
        title: "products",
        route: "product-analytics",
        action: "read",
        subject: "analytics",
      },
      {
        title: "sales",
        route: "sale-analytics",
        action: "read",
        subject: "analytics",
      },
      {
        title: "purchases",
        route: "purchase-analytics",
        action: "read",
        subject: "analytics",
      },
      {
        title: "users",
        route: "user-analytics",
        action: "read",
        subject: "analytics",
      },
    ],
  },
];
