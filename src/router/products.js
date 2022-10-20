/* eslint-disable no-unused-vars */
import ProductsView from "../views/products/ProductsView.vue";
import CreateProductView from "../views/products/CreateProductView.vue";
import ProductDetailsView from "../views/products/ProductDetailsView.vue";
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
    component: CreateProductView,
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
