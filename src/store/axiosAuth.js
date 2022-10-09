import axios from "axios";

const instance = axios.create({
  baseURL: "http://localhost:5000",
  headers: {
    "x-access-token": {
      toString() {
        return `${localStorage.getItem("token")}`;
      },
    },
  },
});

export default instance;
