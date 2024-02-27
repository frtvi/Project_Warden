#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/sha.h>

// Code by V. Barbosa

// Função para calcular o hash SHA-256 de um arquivo
int calcularHashSHA256(const char *nomeArquivo, unsigned char hash[SHA256_DIGEST_LENGTH]) {
    FILE *arquivo = fopen(nomeArquivo, "rb");
    if (!arquivo) {
        perror("Erro ao abrir o arquivo");
        return 0;
    }

    SHA256_CTX ctx;
    SHA256_Init(&ctx);

    const size_t tamanhoBloco = 8192;
    unsigned char bloco[tamanhoBloco];

    size_t bytesLidos;
    while ((bytesLidos = fread(bloco, 1, tamanhoBloco, arquivo))) {
        SHA256_Update(&ctx, bloco, bytesLidos);
    }

    SHA256_Final(hash, &ctx);

    fclose(arquivo);
    return 1;
}

// Função para comparar dois hashes
int compararHashes(const unsigned char hash1[SHA256_DIGEST_LENGTH], const unsigned char hash2[SHA256_DIGEST_LENGTH]) {
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        if (hash1[i] != hash2[i]) {
            return 0; // Hashes são diferentes
        }
    }
    return 1; // Hashes são iguais
}

int main() {
    int opcao;

    do {
        // Tela inicial em ASCII art
        printf("=====================================\n");
        printf("     Bem-vindo ao Secure Checker\n");
        printf("=====================================\n");
        printf("       /\\_/\\  \\    /\\_/\\ \n");
        printf("      ( o.o ) |  ( o.o )\n");
        printf("       > ^ <  >   > ^ <\n\n");

        // Opções
        printf("Opcoes:\n");
        printf("1. Escolher arquivo\n");
        printf("2. Comparar arquivos\n");
        printf("3. Sair\n");

        // Solicitar a escolha do usuário
        printf("\nDigite o numero da opcao desejada: ");
        scanf("%d", &opcao);

        // Realizar a ação correspondente à escolha
        switch (opcao) {
            case 1: {
                // Buffer para armazenar o caminho do arquivo
                char caminhoArquivo[100];

                // Solicitar ao usuário para inserir o caminho do arquivo
                printf("Insira o caminho do arquivo: ");
                scanf("%s", caminhoArquivo);

                // Calcular o hash SHA-256 do arquivo
                unsigned char hashArquivo[SHA256_DIGEST_LENGTH];
                if (calcularHashSHA256(caminhoArquivo, hashArquivo)) {
                    printf("\nHash SHA-256 do arquivo '%s':\n", caminhoArquivo);

                    // Exibir o hash calculado
                    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
                        printf("%02x", hashArquivo[i]);
                    }
                    printf("\n");
                }

                break;
            }
            case 2: {
                // Buffer para armazenar os caminhos dos arquivos
                char caminhoArquivo1[100];
                char caminhoArquivo2[100];

                // Solicitar ao usuário para inserir os caminhos dos arquivos
                printf("Insira o caminho do primeiro arquivo: ");
                scanf("%s", caminhoArquivo1);
                printf("Insira o caminho do segundo arquivo: ");
                scanf("%s", caminhoArquivo2);

                // Calcular os hashes SHA-256 dos arquivos
                unsigned char hashArquivo1[SHA256_DIGEST_LENGTH];
                unsigned char hashArquivo2[SHA256_DIGEST_LENGTH];

                if (calcularHashSHA256(caminhoArquivo1, hashArquivo1) && calcularHashSHA256(caminhoArquivo2, hashArquivo2)) {
                    // Comparar os hashes e exibir o resultado
                    if (compararHashes(hashArquivo1, hashArquivo2)) {
                        printf("\nOs arquivos sao iguais.\n");
                    } else {
                        printf("\nOs arquivos sao diferentes.\n");
                    }
                }

                break;
            }
            case 3:
                printf("Saindo do programa. Ate breve!\n");
                break;
            default:
                printf("Opcao invalida. Tente novamente.\n");
        }

    } while (opcao != 3);

    return 0;
}
