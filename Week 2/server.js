const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.json());

let books = [
    { id: 1, title: "Sgk toán", author: "NXB GD", status: "Có sẵn" },
    { id: 2, title: "Sgk anh", author: "NXB GD", status: "Đã mượn" }
];

app.get('/api/books', async (req, res) => {
    try {
        res.status(200).json(books);
    } catch (error) {
        res.status(500).json({ message: "Lỗi server" });
    }
});

app.post('/api/books', async (req, res) => {
    try {
        const newBook = {
            id: books.length + 1,
            title: req.body.title,
            author: req.body.author,
            status: req.body.status || "Có sẵn"
        };
        books.push(newBook);
        res.status(201).json({ message: "Thêm sách thành công", data: newBook });
    } catch (error) {
        res.status(500).json({ message: "Lỗi thêm sách" });
    }
});

app.put('/api/books/:id', async (req, res) => {
    try {
        const bookId = parseInt(req.params.id);
        const bookIndex = books.findIndex(b => b.id === bookId);

        if (bookIndex === -1) {
            return res.status(404).json({ message: "Không tìm thấy sách" });
        }

        books[bookIndex] = {
            id: bookId,
            title: req.body.title,
            author: req.body.author,
            status: req.body.status
        };
        res.status(200).json({ message: "Cập nhật toàn bộ thành công", data: books[bookIndex] });
    } catch (error) {
        res.status(500).json({ message: "Lỗi server" });
    }
});

app.patch('/api/books/:id', async (req, res) => {
    try {
        const bookId = parseInt(req.params.id);
        const bookIndex = books.findIndex(b => b.id === bookId);

        if (bookIndex === -1) {
            return res.status(404).json({ message: "Không tìm thấy sách" });
        }

        if (req.body.status) books[bookIndex].status = req.body.status;
        if (req.body.title) books[bookIndex].title = req.body.title;

        res.status(200).json({ message: "Cập nhật trạng thái thành công", data: books[bookIndex] });
    } catch (error) {
        res.status(500).json({ message: "Lỗi server" });
    }
});

app.delete('/api/books/:id', async (req, res) => {
    try {
        const bookId = parseInt(req.params.id);
        const bookIndex = books.findIndex(b => b.id === bookId);

        if (bookIndex === -1) {
            return res.status(404).json({ message: "Không tìm thấy sách" });
        }

        books.splice(bookIndex, 1);
        res.status(200).json({ message: "Xóa sách thành công" });
    } catch (error) {
        res.status(500).json({ message: "Lỗi server" });
    }
});

app.listen(PORT, () => {
    console.log(`Server đang chạy tại http://localhost:${PORT}`);
});