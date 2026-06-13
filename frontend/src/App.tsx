import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import Login from './pages/Auth/Login'
import Register from './pages/Auth/Register'
import Feed from './pages/Feed/Feed'
import Profile from './pages/Profile/Profile'
import Navbar from './components/Navbar'

function App() {
  const { isAuthenticated } = useAuthStore()

  return (
    <Router>
      {isAuthenticated && <Navbar />}
      <Routes>
        {!isAuthenticated ? (
          <>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="*" element={<Navigate to="/login" />} />
          </>
        ) : (
          <>
            <Route path="/" element={<Feed />} />
            <Route path="/profile/:userId" element={<Profile />} />
            <Route path="/my-profile" element={<Profile isMyProfile={true} />} />
            <Route path="*" element={<Navigate to="/" />} />
          </>
        )}
      </Routes>
    </Router>
  )
}

export default App
