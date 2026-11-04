// A tiny compiler: source text -> tokens -> tree (AST) -> bytecode -> run on a stack
#include <iostream>
#include <string>
#include <vector>
#include <cctype>

enum class TokenType { Var, Identifier, Number, Equal, Plus, Star, Semicolon, End };

struct Token
{
    TokenType type;
    std::string text;
};

// ---------- 1. Scanner: characters -> tokens
std::vector<Token> Scan(const std::string& source)
{
    std::vector<Token> tokens;
    size_t i = 0;
    while (i < source.size())
    {
        char c = source[i];
        if (isspace(c))
        {
            i++;
            continue;
        }
        if (isdigit(c))
        {
            size_t start = i;
            while (i < source.size() && isdigit(source[i]))
                i++;
            tokens.push_back({ TokenType::Number, source.substr(start, i - start) });
            continue;
        }
        if (isalpha(c))
        {
            size_t start = i;
            while (i < source.size() && isalnum(source[i]))
                i++;
            std::string word = source.substr(start, i - start);
            tokens.push_back({ word == "var" ? TokenType::Var : TokenType::Identifier, word });
            continue;
        }
        if (c == '=') tokens.push_back({ TokenType::Equal, "=" });
        if (c == '+') tokens.push_back({ TokenType::Plus, "+" });
        if (c == '*') tokens.push_back({ TokenType::Star, "*" });
        if (c == ';') tokens.push_back({ TokenType::Semicolon, ";" });
        i++;
    }
    tokens.push_back({ TokenType::End, "end" });
    return tokens;
}

// ---------- 2. Parser: tokens -> tree
struct Node
{
    char kind;            // 'n' number, 'v' variable, '+' add, '*' multiply
    int value;
    std::string name;
    Node* left;
    Node* right;
};

struct Parser
{
    std::vector<Token> tokens;
    size_t pos = 0;

    Token Advance()
    {
        return tokens[pos++];
    }

    bool Match(TokenType type)
    {
        if (tokens[pos].type != type)
            return false;
        pos++;
        return true;
    }

    Node* Primary()
    {
        Token t = Advance();
        if (t.type == TokenType::Number)
            return new Node{ 'n', std::stoi(t.text), "", nullptr, nullptr };
        return new Node{ 'v', 0, t.text, nullptr, nullptr };
    }

    Node* Multiplication()
    {
        Node* left = Primary();
        while (Match(TokenType::Star))
            left = new Node{ '*', 0, "", left, Primary() };
        return left;
    }

    Node* Addition()
    {
        Node* left = Multiplication();
        while (Match(TokenType::Plus))
            left = new Node{ '+', 0, "", left, Multiplication() };
        return left;
    }
};

void PrintTree(Node* node, int depth)
{
    std::string pad(depth * 4, ' ');
    if (node->kind == 'n')
        std::cout << pad << node->value << std::endl;
    else if (node->kind == 'v')
        std::cout << pad << node->name << std::endl;
    else
    {
        std::cout << pad << "[" << node->kind << "]" << std::endl;
        PrintTree(node->left, depth + 1);
        PrintTree(node->right, depth + 1);
    }
}

// ---------- 3. Compiler: tree -> bytecode
struct Instruction
{
    std::string op;
    int arg;
};

std::vector<Instruction> code;
std::vector<std::string> variables;

int VariableIndex(const std::string& name)
{
    for (size_t i = 0; i < variables.size(); i++)
        if (variables[i] == name)
            return (int)i;
    variables.push_back(name);
    return (int)variables.size() - 1;
}

void Compile(Node* node)
{
    if (node->kind == 'n')
        code.push_back({ "LOAD_INT", node->value });
    else if (node->kind == 'v')
        code.push_back({ "LOAD_VAR", VariableIndex(node->name) });
    else
    {
        Compile(node->left);
        Compile(node->right);
        code.push_back({ node->kind == '+' ? "ADD" : "MULTIPLY", 0 });
    }
}

// ---------- 4. Virtual machine: run the bytecode on a stack
void Run()
{
    std::vector<int> stack;
    std::vector<int> registers(variables.size(), 0);
    for (const Instruction& in : code)
    {
        if (in.op == "LOAD_INT")
            stack.push_back(in.arg);
        else if (in.op == "LOAD_VAR")
            stack.push_back(registers[in.arg]);
        else if (in.op == "STORE_VAR")
        {
            registers[in.arg] = stack.back();
            stack.pop_back();
        }
        else if (in.op == "PRINT")
        {
            std::cout << "  result: " << stack.back() << std::endl;
            stack.pop_back();
            continue;
        }
        else
        {
            int b = stack.back();
            stack.pop_back();
            int a = stack.back();
            stack.pop_back();
            stack.push_back(in.op == "ADD" ? a + b : a * b);
        }
        std::cout << "  " << in.op << " " << in.arg << "   stack: [";
        for (size_t i = 0; i < stack.size(); i++)
            std::cout << (i ? ", " : "") << stack[i];
        std::cout << "]" << std::endl;
    }
}

int main()
{
    std::string source = "var x = 1 + 2 * 3; x * 2;";
    std::cout << "source: " << source << std::endl;

    std::vector<Token> tokens = Scan(source);
    std::cout << "tokens:";
    for (const Token& t : tokens)
        std::cout << " [" << t.text << "]";
    std::cout << std::endl;

    Parser parser{ tokens };
    while (!parser.Match(TokenType::End))
    {
        if (parser.Match(TokenType::Var))
        {
            std::string name = parser.Advance().text;
            parser.Match(TokenType::Equal);
            Node* tree = parser.Addition();
            parser.Match(TokenType::Semicolon);
            std::cout << "tree for " << name << " =" << std::endl;
            PrintTree(tree, 1);
            Compile(tree);
            code.push_back({ "STORE_VAR", VariableIndex(name) });
        }
        else
        {
            Node* tree = parser.Addition();
            parser.Match(TokenType::Semicolon);
            std::cout << "tree for print =" << std::endl;
            PrintTree(tree, 1);
            Compile(tree);
            code.push_back({ "PRINT", 0 });
        }
    }

    std::cout << "bytecode:" << std::endl;
    for (const Instruction& in : code)
        std::cout << "  " << in.op << " " << in.arg << std::endl;

    std::cout << "run:" << std::endl;
    Run();
    return 0;
}
