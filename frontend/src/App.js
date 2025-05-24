import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import UserList from './pages/UserList';
import UserDetail from './pages/UserDetail';

function App() {
  return (
    <Router>
      <Routes>
          <Route path="/" element={<UserList />} />
          <Route path="/:id" element={<UserDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
