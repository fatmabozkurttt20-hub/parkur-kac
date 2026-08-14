if not game_started:
        title = big_font.render("PARKUR KAC", True, BLUE)
        info = font.render("Baslamak icin dokun", True, WHITE)
        best_text = font.render(f"En iyi: {best_score}", True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(best_text, (WIDTH // 2 - best_text.get_width() // 2, HEIGHT // 2 + 30))

    elif game_over:
        over_text = big_font.render("DUSTUN!", True, RED)
        score_text = font.render(f"Skor: {score}", True, WHITE)
        best_text = font.render(f"En iyi: {best_score}", True, YELLOW)
        restart_text = font.render("Tekrar denemek icin dokun", True, WHITE)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 30))
        screen.blit(best_text, (WIDTH // 2 - best_text.get_width() // 2, HEIGHT // 2 + 10))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))

    else:
        for obs in obstacles:
            color = RED if obs["kind"] == "jump" else (255, 140, 60)
            pygame.draw.rect(screen, color, (obs["x"], obs["y"], obs["w"], obs["h"]))

        pr = get_player_rect()
        pygame.draw.rect(screen, BLUE, pr)

        score_text = font.render(f"Skor: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        best_text = font.render(f"En iyi: {best_score}", True, YELLOW)
        screen.blit(best_text, (10, 45))

    pygame.display.flip()

pygame.quit()