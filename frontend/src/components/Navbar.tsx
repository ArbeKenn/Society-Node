import { Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

const Navbar = () => {
  const { logout, user } = useAuthStore()

  return (
    <nav className="bg-gradient-to-r from-primary to-secondary text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <span className="text-2xl font-bold">🌐 Society Node</span>
          </Link>

          <div className="flex items-center space-x-4">
            <Link
              to="/"
              className="hover:bg-white hover:bg-opacity-20 px-3 py-2 rounded-md transition"
            >
              Feed
            </Link>
            <Link
              to="/my-profile"
              className="hover:bg-white hover:bg-opacity-20 px-3 py-2 rounded-md transition"
            >
              {user?.username || 'Profile'}
            </Link>
            <button
              onClick={logout}
              className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded-md transition font-semibold"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
