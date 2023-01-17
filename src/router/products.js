/* eslint-disable no-unused-vars */
const ProductsView = () => import("../views/products/ProductsView.vue");
const CreateProductView = () =>
  import("../views/products/CreateProductView.vue");
const ProductDetailsView = () =>
  import("../views/products/ProductDetailsView.vue");
export default [
  {
    path: "/products",
    name: "products",
    component: ProductsView,
    meta: {
      title: "products",
      breadcrumb: [
        {
          text: (route) => "products",
          to: "products",
          active: true,
        },
      ],
    },
  },
  {
    path: "/products/create",
    name: "new-product",
    component: ProductDetailsView,
    meta: {
      title: "createProduct",
      breadcrumb: [
        {
          text: (route) => "products",
          to: "products",
          active: false,
        },
        {
          text: (route) => "createProduct",
          to: "new-product",
          active: true,
        },
      ],
    },
  },
  {
    path: "/products/:productId",
    name: "product-view",
    component: ProductDetailsView,
    meta: {
      title: "productDetails",
      breadcrumb: [
        {
          text: (route) => "products",
          to: "products",
          active: false,
        },
        {
          text: (route) => `${route.meta.title}`,
          to: "product-view",
          active: true,
        },
      ],
    },
  },
];
