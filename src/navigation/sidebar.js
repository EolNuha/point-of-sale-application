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
    subject: "product",
    children: [
      {
        title: "newProduct",
        route: "new-product",
        action: "write",
        subject: "product",
      },
      {
        title: "productList",
        route: "products",
        action: "read",
        subject: "product",
      },
    ],
  },
  {
    title: "sales",
    icon: "ShoppingCartIcon",
    action: "read",
    subject: "sale",
    children: [
      {
        title: "newSale",
        route: "new-sale",
        action: "write",
        subject: "sale",
      },
      {
        title: "salesList",
        route: "sales",
        action: "read",
        subject: "sale",
      },
    ],
  },
  {
    title: "purchases",
    icon: "BuildingStorefrontIcon",
    action: "read",
    subject: "purchase",
    children: [
      {
        title: "newPurchase",
        route: "new-purchase",
        action: "write",
        subject: "purchase",
      },
      {
        title: "purchasesList",
        route: "purchases",
        action: "read",
        subject: "purchase",
      },
    ],
  },
  {
    title: "users",
    icon: "UserGroupIcon",
    action: "read",
    subject: "user",
    children: [
      {
        title: "newUser",
        route: "new-user",
        action: "write",
        subject: "user",
      },
      {
        title: "usersList",
        route: "users",
        action: "read",
        subject: "user",
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
        subject: "user",
      },
    ],
  },
];
