import { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import {
  Container, Typography, Grid, Card, CardContent, Avatar, Pagination
} from '@mui/material';

function UserList() {
  const [users, setUsers] = useState([]);
  const [page, setPage] = useState(1);
  const [count, setCount] = useState(1);

  useEffect(() => {
    axios.get(`http://localhost:8000/?page=${page}`)
      .then(res => {
        setUsers(res.data.results);
        setCount(Math.ceil(res.data.count / 10));
      });
  }, [page]);

    return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Users
      </Typography>
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
};
export default UserList;
