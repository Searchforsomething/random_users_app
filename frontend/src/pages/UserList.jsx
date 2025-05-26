import { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import {
  Container, Typography, Grid, Card, CardContent, Avatar,
  Pagination, TextField, Button, Box
} from '@mui/material';

function UserList() {
  const [users, setUsers] = useState([]);
  const [page, setPage] = useState(1);
  const [count, setCount] = useState(1);
  const [loadCount, setLoadCount] = useState(100);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    axios.get(`http://localhost:8000/?page=${page}`)
      .then(res => {
        setUsers(res.data.results);
        setCount(Math.ceil(res.data.count / 10));
      });
  }, [page]);

  const handleLoadUsers = async () => {
    try {
      setLoading(true);
      const res = await axios.post('http://localhost:8000/load_users/', {
        count: loadCount
      });
      alert(res.data.message);
      setPage(1);
    } catch (error) {
      alert("Error loading users: " + error.response?.data?.message || error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Users
      </Typography>

      <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
        <TextField
          label="Amount of users"
          type="number"
          value={loadCount}
          onChange={(e) => setLoadCount(Number(e.target.value))}
          inputProps={{ min: 1 }}
        />
        <Button
          variant="contained"
          onClick={handleLoadUsers}
          disabled={loading}
        >
          {loading ? "Loading..." : "Load users"}
        </Button>
      </Box>

      <Grid container spacing={2}>
        {users.map(user => (
          <Grid item xs={12} sm={6} md={4} key={user.id}>
            <Card component={Link} to={`/${user.id}`} sx={{ textDecoration: 'none' }}>
              <CardContent sx={{ display: 'flex', alignItems: 'center' }}>
                <Avatar src={user.thumbnail} sx={{ mr: 2 }} />
                <div>
                  <Typography variant="subtitle1">{user.first_name} {user.last_name}</Typography>
                  <Typography variant="body2" color="text.secondary">{user.email}</Typography>
                </div>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Pagination
        count={count}
        page={page}
        onChange={(e, val) => setPage(val)}
        sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}
      />
    </Container>
  );
}

export default UserList;
