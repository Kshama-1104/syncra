import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 15000,
});

api.interceptors.request.use((config) => {
  const access = localStorage.getItem("syncra_access");
  if (access) config.headers.Authorization = `Bearer ${access}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original?._retry) {
      original._retry = true;
      const refresh = localStorage.getItem("syncra_refresh");
      if (!refresh) throw error;
      const { data } = await axios.post(`${import.meta.env.VITE_API_URL}/token/refresh/`, { refresh });
      localStorage.setItem("syncra_access", data.access);
      original.headers.Authorization = `Bearer ${data.access}`;
      return api(original);
    }
    throw error;
  }
);
