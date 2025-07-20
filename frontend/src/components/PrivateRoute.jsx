import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ children }) => {
  const user = JSON.parse(localStorage.getItem('user'));
  return user && user.token ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
