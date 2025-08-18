import axios from 'axios'

const api = axios.create({
  baseURL:
    window.location.hostname === "localhost"
      ? "http://localhost:5000"
      : "https://rua11store-catalog-api-lbp7.onrender.com",
  headers: {
    "Content-Type": "application/json",
  },
});

// Funções para manipular tokens no localStorage
function getAccessToken() {
  return localStorage.getItem('access_token');
}

function getRefreshToken() {
  return localStorage.getItem('refresh_token');
}

function setAccessToken(token) {
  localStorage.setItem('access_token', token);
}

function logout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  window.location.href = '/login';  // ou onde for sua página de login
}

//Inteceptor
api.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;

        //If 401 error
        if(error.response?.status === 401 && !originalRequest._retry){
            originalRequest._retry = true;

            const RefreshToken = getRefreshToken();

            if(!RefreshToken){
                logout()
                return Promisse.reject(error);
            }
            try{
                const response = await axios.post(
                    api.defaults.baseURL + '/refresh',
                    null,
                    {
                        headers: {
                            Authorization: `Bearer ${refreshToken}`,
                        }
                    }
                );

                const newAccessToken = response.data.access_token;
                setAccessToken(newAccessToken);

                //update header request
                originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
                return api(originalRequest);
            }
            catch(refreshError){
                logout();
                return Promisse.reject(refreshError);
            }
        }
        return Promisse.reject(error);
    }

);

export default api;