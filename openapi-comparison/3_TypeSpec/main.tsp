import "@typespec/http";
import "@typespec/openapi3";

using TypeSpec.Http;

@service(#{
  title: "Library Management API"
})
namespace Library;

model Book {
  id: string;
  title: string;
  author: string;
}

model BookInput {
  title: string;
  author: string;
}

@route("/books")
interface Books {
  @summary("Lấy danh sách sách")
  @get list(): Book[];

  @summary("Thêm sách mới")
  @post create(@body book: BookInput): { @statusCode _: 201, @body body: Book };
}