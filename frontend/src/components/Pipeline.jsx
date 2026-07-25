import { Card, CardContent, Typography } from "@mui/material";

export default function Pipeline() {
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
        <Typography variant="h6">AI Detection Pipeline</Typography>
      </CardContent>
    </Card>
  );
}