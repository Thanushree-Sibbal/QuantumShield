import { Card, CardContent, Typography } from "@mui/material";

export default function AlertPanel() {
  return (
    <Card
      sx={{
        background: "#151C32",
        color: "white",
        border: "1px solid #27314E",
        minHeight: 300,
      }}
    >
      <CardContent>
        <Typography variant="h6">Alert Center</Typography>
      </CardContent>
    </Card>
  );
}